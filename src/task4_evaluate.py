#!/usr/bin/env python3
"""
Task 4: Evaluate Kosmos MOLECULES results
Parse molecular designs and calculate evaluation metrics
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Try to import RDKit for SMILES validation and QED calculation
try:
    from rdkit import Chem
    from rdkit.Chem import QED, Descriptors, Lipinski
    RDKIT_AVAILABLE = True
    print("✅ RDKit is available for chemical analysis")
except ImportError:
    RDKIT_AVAILABLE = False
    print("⚠️ RDKit not available - using basic validation only")

# Load ground truth
with open("input/task4_ground_truth.json", "r") as f:
    ground_truth = json.load(f)

baseline = ground_truth["nirmatrelvir"]


def validate_smiles(smiles_str):
    """Check if SMILES string is chemically valid."""
    if not RDKIT_AVAILABLE:
        # Basic check for non-empty string
        return bool(smiles_str and len(smiles_str) > 5)

    try:
        mol = Chem.MolFromSmiles(smiles_str)
        return mol is not None
    except:
        return False


def calculate_qed(smiles_str):
    """Calculate QED score if RDKit available."""
    if not RDKIT_AVAILABLE:
        return None

    try:
        mol = Chem.MolFromSmiles(smiles_str)
        if mol:
            return QED.qed(mol)
    except:
        pass
    return None


def count_lipinski_violations(smiles_str):
    """Count Lipinski rule violations if RDKit available."""
    if not RDKIT_AVAILABLE:
        return None

    try:
        mol = Chem.MolFromSmiles(smiles_str)
        if mol:
            # Calculate Lipinski parameters
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = Lipinski.NumHDonors(mol)
            hba = Lipinski.NumHAcceptors(mol)

            violations = 0
            if mw > 500: violations += 1
            if logp > 5: violations += 1
            if hbd > 5: violations += 1
            if hba > 10: violations += 1

            return violations
    except:
        pass
    return None


def extract_properties_from_text(text, molecule_name="Molecule"):
    """Extract properties from text response."""
    properties = {}

    # Extract SMILES (look for patterns like "SMILES: ..." or "CC(C)...")
    smiles_patterns = [
        r"SMILES:\s*([^\s\n]+)",
        r"smiles[:\s]*([^\s\n]+)",
        r"([A-Za-z0-9@+\-\[\]\(\)\\\/%=#$]+)\s*\n",
    ]

    for pattern in smiles_patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Validate each potential SMILES
            for match in matches:
                if validate_smiles(match):
                    properties["smiles"] = match
                    break
            if "smiles" in properties:
                break

    # Extract numerical properties
    # Solubility (μg/mL)
    sol_match = re.search(r"solubility[:\s]*([0-9.]+)\s*(?:ug\/ml|μg\/ml|microgram)", text, re.IGNORECASE)
    if sol_match:
        properties["solubility_ugml"] = float(sol_match.group(1))

    # Oral bioavailability (%)
    bio_match = re.search(r"oral bioavailability[:\s]*([0-9.]+)\s*(?:%|percent)", text, re.IGNORECASE)
    if bio_match:
        properties["oral_bioavailability_pct"] = float(bio_match.group(1))

    # Permeability (Caco-2)
    perm_match = re.search(r"permeability[:\s]*([0-9.]+)\s*(?:×\s*10\^-?\d*|cm\/s|10\^-?\d*)", text, re.IGNORECASE)
    if perm_match:
        properties["caco2_permeability"] = float(perm_match.group(1))

    # QED score
    qed_match = re.search(r"QED[:\s]*([0-9.]+)", text, re.IGNORECASE)
    if qed_match:
        properties["qed_score"] = float(qed_match.group(1))

    # CYP3A4 inhibition
    cyp_inhibit = re.search(r"CYP3A4\s*(?:inhibitor|inhibition)", text, re.IGNORECASE)
    if cyp_inhibit:
        properties["cyp3a4_inhibitor"] = True
    else:
        cyp_no_inhibit = re.search(r"(?:not|no)\s+CYP3A4\s*(?:inhibitor|inhibition)", text, re.IGNORECASE)
        properties["cyp3a4_inhibitor"] = False if cyp_no_inhibit else None

    # Synthetic accessibility score
    sas_match = re.search(r"SAS[:\s]*([0-9.]+)", text, re.IGNORECASE)
    if sas_match:
        properties["sascore"] = float(sas_match.group(1))

    return properties


def count_synthesis_steps(text):
    """Count steps in retrosynthesis route."""
    # Look for step indicators
    step_patterns = [
        r"step\s+(\d+)",
        r"(\d+)\.\s*",
        r"→|-->|⟶|->",
        r"reaction\s+(\d+)",
    ]

    max_step = 0
    for pattern in step_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                try:
                    step_num = int(match)
                    max_step = max(max_step, step_num)
                except:
                    pass

    # If no numbered steps, count arrow indicators
    if max_step == 0:
        arrows = re.findall(r"→|-->|⟶|->", text)
        max_step = len(arrows) + 1

    return max_step


def check_property_improvements(molecule, baseline):
    """Count how many properties improved over baseline."""
    improvements = 0

    # Solubility improvement
    if molecule.get("solubility_ugml", 0) > baseline["admet"]["solubility_ugml"]:
        improvements += 1
        molecule["improved_solubility"] = True
    else:
        molecule["improved_solubility"] = False

    # Oral bioavailability improvement
    if molecule.get("oral_bioavailability_pct", 0) > baseline["admet"]["oral_bioavailability_pct"]:
        improvements += 1
        molecule["improved_bioavailability"] = True
    else:
        molecule["improved_bioavailability"] = False

    # QED score improvement
    mol_qed = molecule.get("qed_score")
    if mol_qed and mol_qed > baseline["drug_likeness"]["qed_score"]:
        improvements += 1
        molecule["improved_qed"] = True
    else:
        molecule["improved_qed"] = False

    # CYP3A4 inhibition improvement (not being an inhibitor is better)
    if molecule.get("cyp3a4_inhibitor") is False:
        improvements += 1
        molecule["improved_cyp"] = True
    elif molecule.get("cyp3a4_inhibitor") is True:
        molecule["improved_cyp"] = False

    molecule["total_improvements"] = improvements
    return improvements


def verify_admet_completeness(molecule):
    """Check if molecule has all required ADMET predictions."""
    required = ["solubility_ugml", "oral_bioavailability_pct"]
    optional = ["qed_score", "cyp3a4_inhibitor", "caco2_permeability"]

    has_required = all(prop in molecule for prop in required)
    has_optional = sum(1 for prop in optional if prop in molecule)

    return has_required, has_optional


def main():
    """Main evaluation function."""
    print("\n" + "="*60)
    print("TASK 4: STRUCTURAL BIOLOGY - EVALUATION")
    print("="*60)
    print(f"\nStart time: {datetime.now()}")

    # Load Kosmos results
    results_file = Path("output/task4_results/kosmos_raw_output.json")

    if not results_file.exists():
        print(f"\n❌ Error: Results file not found at {results_file}")
        print("Please wait for the MOLECULES job to complete.")
        print(f"Task ID: 46d09be4-cbe6-4138-837e-54766594fd4a")
        sys.exit(1)

    with open(results_file, "r") as f:
        kosmos_results = json.load(f)

    print(f"\n✅ Loaded Kosmos results")

    # Parse molecules from results
    molecules = []

    # Try different result formats
    if isinstance(kosmos_results, dict):
        if "result" in kosmos_results:
            result_text = str(kosmos_results["result"])
        elif "molecules" in kosmos_results:
            result_text = json.dumps(kosmos_results["molecules"])
        else:
            result_text = json.dumps(kosmos_results)
    else:
        result_text = str(kosmos_results)

    # Split into individual molecules (look for numbered items or "Molecule" labels)
    molecule_sections = []

    # Try to split by molecule indicators
    patterns = [
        r"Molecule\s+\d+[:\n]",
        r"Molecule\s+[A-C][:\n]",
        r"Design\s+\d+[:\n]",
        r"\d+\.\s*[A-Za-z]",
    ]

    for pattern in patterns:
        matches = list(re.finditer(pattern, result_text, re.IGNORECASE))
        if matches:
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(result_text)
                molecule_sections.append(result_text[start:end])
            break

    # If no clear sections, treat whole response as one molecule
    if not molecule_sections:
        molecule_sections = [result_text]

    # Parse each molecule
    for i, section in enumerate(molecule_sections[:3]):  # Max 3 molecules
        print(f"\nParsing Molecule {i+1}...")
        mol_props = extract_properties_from_text(section, f"Molecule {i+1}")

        if "smiles" in mol_props:
            # Validate SMILES with RDKit if available
            if RDKIT_AVAILABLE and mol_props["smiles"]:
                qed_score = calculate_qed(mol_props["smiles"])
                if qed_score:
                    mol_props["qed_score_calculated"] = qed_score

                lipinski_violations = count_lipinski_violations(mol_props["smiles"])
                if lipinski_violations is not None:
                    mol_props["lipinski_violations"] = lipinski_violations

            # Count synthesis steps
            mol_props["synthesis_steps"] = count_synthesis_steps(section)

            # Check improvements
            check_property_improvements(mol_props, baseline)

            # Verify completeness
            has_required, has_optional = verify_admet_completeness(mol_props)
            mol_props["has_required_admet"] = has_required
            mol_props["optional_admet_count"] = has_optional

            mol_props["molecule_number"] = i + 1
            molecules.append(mol_props)

            print(f"  - SMILES: {mol_props['smiles'][:50]}...")
            print(f"  - Valid: {validate_smiles(mol_props['smiles'])}")
            print(f"  - Improvements: {mol_props['total_improvements']}/4")
        else:
            print(f"  - No valid SMILES found")

    # Calculate overall metrics
    print(f"\n{'='*60}")
    print("CALCULATING METRICS")
    print("="*60)

    total_molecules = 3
    valid_smiles = sum(1 for mol in molecules if mol.get("smiles") and validate_smiles(mol["smiles"]))
    complete_admet = sum(1 for mol in molecules if mol.get("has_required_admet", False))
    with_improvements = sum(1 for mol in molecules if mol.get("total_improvements", 0) >= 1)
    with_synthesis = sum(1 for mol in molecules if mol.get("synthesis_steps", 0) > 0)

    metrics = {
        "chemical_validity_pct": (valid_smiles / total_molecules) * 100,
        "admet_completeness_pct": (complete_admet / total_molecules) * 100,
        "property_improvement_pct": (with_improvements / total_molecules) * 100,
        "synthesis_provided_pct": (with_synthesis / total_molecules) * 100,
        "valid_molecules": valid_smiles,
        "complete_admet_molecules": complete_admet,
        "molecules_with_improvements": with_improvements,
        "molecules_with_synthesis": with_synthesis,
        "total_molecules": total_molecules,
        "evaluation_timestamp": datetime.now().isoformat()
    }

    # Save metrics
    metrics_file = Path("output/task4_results/metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n✅ Metrics saved to: {metrics_file}")

    # Save parsed molecules
    molecules_file = Path("output/task4_results/parsed_molecules.json")
    with open(molecules_file, "w") as f:
        json.dump(molecules, f, indent=2)

    print(f"✅ Parsed molecules saved to: {molecules_file}")

    # Print summary
    print(f"\n{'='*60}")
    print("EVALUATION SUMMARY")
    print("="*60)

    print(f"\nBaseline: Nirmatrelvir (Paxlovid)")
    print(f"  - SMILES: {baseline['smiles'][:50]}...")
    print(f"  - Molecular weight: {baseline['molecular_weight']} g/mol")
    print(f"  - Oral bioavailability: {baseline['admet']['oral_bioavailability_pct']}%")
    print(f"  - Solubility: {baseline['admet']['solubility_ugml']} μg/mL")
    print(f"  - QED score: {baseline['drug_likeness']['qed_score']}")
    print(f"  - CYP3A4 inhibitor: {baseline['admet']['cyp3a4_inhibitor']}")

    print(f"\nDesigned Molecules:")
    for mol in molecules:
        print(f"\nMolecule {mol['molecule_number']}:")
        print(f"  - SMILES: {mol.get('smiles', 'N/A')}")
        print(f"  - Valid: {validate_smiles(mol.get('smiles', ''))}")
        print(f"  - Oral bioavailability: {mol.get('oral_bioavailability_pct', 'N/A')}%")
        print(f"  - Solubility: {mol.get('solubility_ugml', 'N/A')} μg/mL")
        print(f"  - QED score: {mol.get('qed_score', mol.get('qed_score_calculated', 'N/A'))}")
        print(f"  - CYP3A4 inhibitor: {mol.get('cyp3a4_inhibitor', 'N/A')}")
        print(f"  - Improvements: {mol.get('total_improvements', 0)}/4")
        print(f"  - Synthesis steps: {mol.get('synthesis_steps', 0)}")

    print(f"\nMetrics:")
    print(f"  - Chemical validity: {metrics['chemical_validity_pct']:.1f}% ({metrics['valid_molecules']}/{metrics['total_molecules']})")
    print(f"  - ADMET completeness: {metrics['admet_completeness_pct']:.1f}% ({metrics['complete_admet_molecules']}/{metrics['total_molecules']})")
    print(f"  - Property improvement: {metrics['property_improvement_pct']:.1f}% ({metrics['molecules_with_improvements']}/{metrics['total_molecules']})")
    print(f"  - Synthesis provided: {metrics['synthesis_provided_pct']:.1f}% ({metrics['molecules_with_synthesis']}/{metrics['total_molecules']})")

    # Determine pass/fail
    passes = [
        metrics['chemical_validity_pct'] >= 100,
        metrics['admet_completeness_pct'] >= 100,
        metrics['property_improvement_pct'] >= 66,
        metrics['synthesis_provided_pct'] >= 100
    ]

    overall_pass = all(passes)
    print(f"\nOverall Assessment: {'✅ PASS' if overall_pass else '❌ FAIL'}")

    if overall_pass:
        print("All targets met!")
    else:
        print("Targets not met:")
        if not passes[0]: print("  - Chemical validity < 100%")
        if not passes[1]: print("  - ADMET completeness < 100%")
        if not passes[2]: print("  - Property improvement < 66%")
        if not passes[3]: print("  - Synthesis provided < 100%")

    return metrics, molecules


if __name__ == "__main__":
    metrics, molecules = main()