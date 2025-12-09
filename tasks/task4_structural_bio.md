# Task 4: Structural Biology - MOLECULES Job

## Objective
Test Kosmos MOLECULES (Phoenix) capability for computational drug design to support grant proposals requiring cheminformatics.

## Context
You are running Experiment 4 of 5 in a Kosmos pilot study. This task tests if Kosmos can generate chemically valid molecular designs with improved properties.

## Your Task

### 1. Run Kosmos MOLECULES Query

**Query:**
```
Design three small molecule inhibitors for the SARS-CoV-2 main protease (Mpro, also called 3CLpro) with improved oral bioavailability compared to nirmatrelvir (Paxlovid). For each molecule:
1. Provide the SMILES structure
2. Calculate ADMET properties (solubility, permeability, oral bioavailability %, CYP metabolism)
3. Predict drug-likeness (QED score, Lipinski's Rule compliance)
4. Propose a retrosynthesis route from commercially available starting materials
5. Estimate synthetic accessibility (SAScore)

Compare each designed molecule's properties to nirmatrelvir baseline.
```

**Use Edison API:**
- Job type: `JobNames.MOLECULES`
- Expected runtime: ~30 minutes
- Cost: ~$200/run

### 2. Parse Results

Extract from Kosmos output for each of 3 molecules:
- **SMILES:** Chemical structure
- **ADMET properties:**
  - Solubility (μg/mL)
  - Permeability (Caco-2, 10^-6 cm/s)
  - Oral bioavailability (F%)
  - CYP interactions
- **Drug-likeness:**
  - QED score (0-1)
  - Lipinski violations
- **Synthesis:**
  - Retrosynthesis steps
  - Starting materials
  - Estimated cost (if provided)
  - Synthetic accessibility score (0-10, lower = easier)

Save to: `output/task4_results/kosmos_raw_output.json`

### 3. Compare to Ground Truth

**Ground Truth - Nirmatrelvir (Paxlovid) properties:**
```json
{
  "nirmatrelvir": {
    "smiles": "CC1(C2C1C(N(C2)C(=O)C(C(C)(C)C)NC(=O)C(F)(F)F)C(=O)NC(CC3CCNC3=O)C#N)C",
    "molecular_weight": 499.53,
    "admet": {
      "solubility_ugml": 135,  // Moderate, ~0.27 mg/mL
      "caco2_permeability": 12.5,  // 10^-6 cm/s, moderate
      "oral_bioavailability_pct": 50,  // ~50% in humans
      "cyp3a4_substrate": true,
      "cyp3a4_inhibitor": true  // Major interaction liability
    },
    "drug_likeness": {
      "qed_score": 0.58,  // Moderate drug-likeness
      "lipinski_violations": 1,  // MW > 500
      "rotatable_bonds": 5
    },
    "synthesis": {
      "sascore": 4.2,  // Moderately complex
      "total_steps": 12  // Multi-step synthesis
    }
  },
  "improvement_targets": {
    "oral_bioavailability": ">50%",
    "solubility": ">135 μg/mL",
    "reduce_cyp3a4_inhibition": true,
    "qed_score": ">0.58"
  }
}
```

Save to: `input/task4_ground_truth.json`

### 4. Calculate Metrics

Run automated evaluation:

```python
# File: src/task4_evaluate.py

from rdkit import Chem
from rdkit.Chem import QED, Descriptors

def validate_smiles(smiles_str):
    """Is SMILES chemically valid?"""
    try:
        mol = Chem.MolFromSmiles(smiles_str)
        return mol is not None
    except:
        return False

def check_property_improvements(molecule, baseline):
    """Count how many properties improved over baseline"""
    improvements = 0

    # Solubility
    if molecule.get("solubility_ugml", 0) > baseline["admet"]["solubility_ugml"]:
        improvements += 1

    # Oral bioavailability
    if molecule.get("oral_bioavailability_pct", 0) > baseline["admet"]["oral_bioavailability_pct"]:
        improvements += 1

    # Drug-likeness
    if molecule.get("qed_score", 0) > baseline["drug_likeness"]["qed_score"]:
        improvements += 1

    # CYP inhibition (improvement = not inhibitor)
    if not molecule.get("cyp3a4_inhibitor", True):  # Default True = no improvement
        improvements += 1

    return improvements

def verify_admet_completeness(molecule):
    """Does molecule have all required ADMET predictions?"""
    required = ["solubility_ugml", "oral_bioavailability_pct", "qed_score"]
    return all(prop in molecule for prop in required)

def count_synthesis_steps(retrosynthesis):
    """Count steps in proposed synthesis route"""
    if isinstance(retrosynthesis, list):
        return len(retrosynthesis)
    elif isinstance(retrosynthesis, str):
        # Heuristic: count arrows or steps mentioned
        import re
        steps = re.findall(r'step \d+|→|-->|⟶', retrosynthesis.lower())
        return len(steps)
    return 0
```

**Metrics to calculate:**
- **Chemical validity:** % of 3 molecules with valid SMILES (target: 100%, i.e., 3/3)
- **ADMET completeness:** % with all required predictions (target: 100%)
- **Property improvement:** % showing ≥1 improved property vs. nirmatrelvir (target: ≥66%, i.e., 2/3)
- **Synthesis provided:** % with retrosynthesis route (target: 100%)

Save to: `output/task4_results/metrics.json`

### 5. Generate Report

Create: `output/task4_results/task4_report.md`

**Template:**
```markdown
# Task 4: Structural Biology - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** {minutes}
- **Cost:** $200

## Kosmos Query
{query text}

## Ground Truth Comparison

### Baseline: Nirmatrelvir (Paxlovid)
| Property | Value |
|----------|-------|
| SMILES | `{smiles}` |
| MW | 499.53 g/mol |
| Solubility | 135 μg/mL |
| Oral bioavailability | 50% |
| QED score | 0.58 |
| CYP3A4 inhibition | Yes (liability) |

### Designed Molecule 1
**SMILES:** `{smiles}`
**Valid:** ✓/✗

| Property | Kosmos Prediction | Nirmatrelvir | Improved? |
|----------|------------------|--------------|-----------|
| Solubility (μg/mL) | {X} | 135 | ✓/✗ |
| Oral bioavailability (%) | {Y} | 50 | ✓/✗ |
| QED score | {Z} | 0.58 | ✓/✗ |
| CYP3A4 inhibitor | {T/F} | Yes | ✓/✗ |

**Total improvements:** {N}/4

**Retrosynthesis:**
{Summary or step count}

**Synthetic accessibility:** {SAScore}

---

### Designed Molecule 2
{Repeat structure}

---

### Designed Molecule 3
{Repeat structure}

---

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Chemical validity | 100% (3/3) | {X}% | PASS/FAIL |
| ADMET completeness | 100% | {Y}% | PASS/FAIL |
| Property improvement | ≥66% (2/3) | {Z}% | PASS/FAIL |
| Synthesis provided | 100% | {W}% | PASS/FAIL |

## Overall Assessment
**PASS/FAIL:** {based on all 4 metrics passing}

## Best Candidate
**Molecule {N}** shows the most improvements:
- {List key improvements}
- Estimated synthetic feasibility: {assessment}

## Comparison Table

| Molecule | Valid SMILES | QED | F% | Solubility | CYP Inhibition | Improvements |
|----------|--------------|-----|----|-----------|--------------------|--------------|
| Nirmatrelvir | ✓ | 0.58 | 50% | 135 | Yes | - |
| Design 1 | ✓/✗ | {X} | {Y}% | {Z} | Yes/No | {N}/4 |
| Design 2 | ✓/✗ | {X} | {Y}% | {Z} | Yes/No | {N}/4 |
| Design 3 | ✓/✗ | {X} | {Y}% | {Z} | Yes/No | {N}/4 |

## Qualitative Observations
{Notes on:
- Chemical plausibility (expert assessment)
- Synthesis feasibility (are routes realistic?)
- Trade-offs (e.g., better solubility but worse permeability)
- Potential for actual lab testing
}

## Molecular Structures
{If possible, include 2D structure images using RDKit}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../logs/task4_execution.log`

## Notes
{Any issues with SMILES parsing, property predictions, synthesis routes}
```

## File Naming Convention
- Source code: `src/task4_*.py`
- Input data: `input/task4_ground_truth.json`
- Outputs: `output/task4_results/*`
- Logs: `logs/task4_execution.log`

## Success Criteria
- [ ] Kosmos job completes successfully
- [ ] 3 molecules designed
- [ ] All 4 metrics calculated
- [ ] Report generated
- [ ] All 4 metrics pass targets
- [ ] At least 1 molecule shows multiple improvements

## If Job Fails
1. Save error message to `logs/task4_error.log`
2. Document failure mode in report
3. If partial results (e.g., 1-2 molecules), evaluate those
4. Mark overall assessment as FAIL if <3 molecules

## Tools Available
- Edison Python SDK
- RDKit (for SMILES validation, QED calculation)
- requests (for PubChem/ChEMBL lookups)
- pytest

## Budget
$200 for this experiment (1 Kosmos MOLECULES run)

## Timeline
Target completion: 45 minutes (30 min Kosmos + 15 min evaluation)

## Additional Notes
- Chemical validity is critical (must use RDKit to verify)
- ADMET predictions are computational estimates (not experimental)
- Retrosynthesis routes should be plausible, not necessarily optimal
- Comparison to nirmatrelvir is key (absolute values matter less than improvements)
- If Kosmos provides confidence intervals or uncertainty, include in report
