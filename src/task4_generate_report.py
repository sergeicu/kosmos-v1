#!/usr/bin/env python3
"""
Task 4: Generate comprehensive report
"""

import json
from datetime import datetime
from pathlib import Path

# Load all data
with open("input/task4_ground_truth.json", "r") as f:
    ground_truth = json.load(f)

with open("output/task4_results/task_id.json", "r") as f:
    task_info = json.load(f)

with open("output/task4_results/kosmos_raw_output.json", "r") as f:
    kosmos_results = json.load(f)

with open("output/task4_results/metrics.json", "r") as f:
    metrics = json.load(f)

with open("output/task4_results/parsed_molecules.json", "r") as f:
    molecules = json.load(f)

baseline = ground_truth["nirmatrelvir"]

# Generate report
report = f"""# Task 4: Structural Biology - Results

## Execution Summary
- **Start time:** {task_info['submitted_at']}
- **End time:** {metrics['evaluation_timestamp']}
- **Task ID:** {task_info['task_id']}
- **Duration:** ~30 minutes
- **Cost:** $200

## Kosmos Query
```
{task_info['query']}
```

## Ground Truth Comparison

### Baseline: Nirmatrelvir (Paxlovid)
| Property | Value |
|----------|-------|
| SMILES | `{baseline['smiles']}` |
| MW | {baseline['molecular_weight']} g/mol |
| Solubility | {baseline['admet']['solubility_ugml']} μg/mL |
| Oral bioavailability | {baseline['admet']['oral_bioavailability_pct']}% |
| QED score | {baseline['drug_likeness']['qed_score']} |
| CYP3A4 inhibition | {'Yes (liability)' if baseline['admet']['cyp3a4_inhibitor'] else 'No'} |
| SAScore | {baseline['synthesis']['sascore']} |
| Total synthesis steps | {baseline['synthesis']['total_steps']} |

"""

# Add each molecule
for mol in molecules:
    mol_num = mol['molecule_number']
    report += f"""
### Designed Molecule {mol_num}
**SMILES:** `{mol.get('smiles', 'N/A')}`
**Valid:** {'✓' if mol.get('smiles') else '✗'}

| Property | Kosmos Prediction | Nirmatrelvir | Improved? |
|----------|------------------|--------------|-----------|
| Solubility (μg/mL) | {mol.get('solubility_ugml', 'N/A')} | {baseline['admet']['solubility_ugml']} | {'✓' if mol.get('improved_solubility') else '✗'} |
| Oral bioavailability (%) | {mol.get('oral_bioavailability_pct', 'N/A')} | {baseline['admet']['oral_bioavailability_pct']} | {'✓' if mol.get('improved_bioavailability') else '✗'} |
| QED score | {mol.get('qed_score', mol.get('qed_score_calculated', 'N/A'))} | {baseline['drug_likeness']['qed_score']} | {'✓' if mol.get('improved_qed') else '✗'} |
| CYP3A4 inhibitor | {mol.get('cyp3a4_inhibitor', 'N/A')} | Yes | {'✓' if mol.get('improved_cyp') else '✗'} |
| Lipinski violations | {mol.get('lipinski_violations', 'N/A')} | {baseline['drug_likeness']['lipinski_violations']} | - |

**Total improvements:** {mol.get('total_improvements', 0)}/4

**Retrosynthesis:**
{mol.get('synthesis_steps', 0)} steps proposed

**Synthetic accessibility:** {mol.get('sascore', 'N/A')}

---

"""

report += f"""
## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Chemical validity | 100% (3/3) | {metrics['chemical_validity_pct']:.1f}% ({metrics['valid_molecules']}/{metrics['total_molecules']}) | {'PASS' if metrics['chemical_validity_pct'] >= 100 else 'FAIL'} |
| ADMET completeness | 100% | {metrics['admet_completeness_pct']:.1f}% ({metrics['complete_admet_molecules']}/{metrics['total_molecules']}) | {'PASS' if metrics['admet_completeness_pct'] >= 100 else 'FAIL'} |
| Property improvement | ≥66% (2/3) | {metrics['property_improvement_pct']:.1f}% ({metrics['molecules_with_improvements']}/{metrics['total_molecules']}) | {'PASS' if metrics['property_improvement_pct'] >= 66 else 'FAIL'} |
| Synthesis provided | 100% | {metrics['synthesis_provided_pct']:.1f}% ({metrics['molecules_with_synthesis']}/{metrics['total_molecules']}) | {'PASS' if metrics['synthesis_provided_pct'] >= 100 else 'FAIL'} |

## Overall Assessment
**{'✅ PASS' if all([metrics['chemical_validity_pct'] >= 100, metrics['admet_completeness_pct'] >= 100, metrics['property_improvement_pct'] >= 66, metrics['synthesis_provided_pct'] >= 100]) else '❌ FAIL'}**

"""

# Find best candidate
best_mol = max(molecules, key=lambda x: x.get('total_improvements', 0)) if molecules else None
if best_mol:
    report += f"""
## Best Candidate
**Molecule {best_mol['molecule_number']}** shows the most improvements ({best_mol.get('total_improvements', 0)}/4):
- SMILES: `{best_mol.get('smiles', 'N/A')}`
- {'Improved solubility' if best_mol.get('improved_solubility') else ''}
- {'Improved oral bioavailability' if best_mol.get('improved_bioavailability') else ''}
- {'Improved QED score' if best_mol.get('improved_qed') else ''}
- {'Reduced CYP3A4 inhibition' if best_mol.get('improved_cyp') else ''}
- Estimated synthetic feasibility: {best_mol.get('synthesis_steps', 0)} steps

"""

report += f"""
## Comparison Table

| Molecule | Valid SMILES | QED | F% | Solubility | CYP Inhibition | Improvements |
|----------|--------------|-----|----|-----------|--------------------|--------------|
| Nirmatrelvir | ✓ | {baseline['drug_likeness']['qed_score']} | {baseline['admet']['oral_bioavailability_pct']}% | {baseline['admet']['solubility_ugml']} | {'Yes' if baseline['admet']['cyp3a4_inhibitor'] else 'No'} | - |
"""

for mol in molecules:
    report += f"""| Design {mol['molecule_number']} | {'✓' if mol.get('smiles') else '✗'} | {mol.get('qed_score', mol.get('qed_score_calculated', 'N/A'))} | {mol.get('oral_bioavailability_pct', 'N/A')}% | {mol.get('solubility_ugml', 'N/A')} | {mol.get('cyp3a4_inhibitor', 'N/A')} | {mol.get('total_improvements', 0)}/4 |\n"""

report += """
## Qualitative Observations
- Chemical plausibility: [To be assessed based on SMILES validity and structural features]
- Synthesis feasibility: [To be assessed based on proposed routes]
- Trade-offs: [To be analyzed after full results]
- Potential for lab testing: [To be evaluated]

## Molecular Structures
[2D structures can be generated from SMILES using RDKit if needed]

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Parsed molecules: `parsed_molecules.json`
- Task ID: `task_id.json`

## Notes
"""

# Add notes about missing RDKit if applicable
try:
    from rdkit import Chem
    from rdkit.Chem import QED, Descriptors, Lipinski
except ImportError:
    report += "- RDKit not installed - limited chemical validation performed\n"

# Add specific notes about each molecule
for mol in molecules:
    if not mol.get('smiles'):
        report += f"- Molecule {mol['molecule_number']}: No valid SMILES found\n"
    if not mol.get('has_required_admet'):
        report += f"- Molecule {mol['molecule_number']}: Missing required ADMET predictions\n"

# Save report
report_file = Path("output/task4_results/task4_report.md")
with open(report_file, "w") as f:
    f.write(report)

print(f"✅ Report generated: {report_file}")
print(f"Overall Assessment: {'PASS' if all([metrics['chemical_validity_pct'] >= 100, metrics['admet_completeness_pct'] >= 100, metrics['property_improvement_pct'] >= 66, metrics['synthesis_provided_pct'] >= 100]) else 'FAIL'}")