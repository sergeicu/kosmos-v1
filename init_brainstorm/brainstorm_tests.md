# Test Design - Kosmos Pilot Experiments

## Testing Philosophy
**TDD Approach:** Write tests first, watch fail, implement minimal code to pass

## Phase 0: API Connectivity (15 min)

### Test Suite
```python
def test_import_edison_client():
    """Can we import the Edison SDK?"""
    from edison_client import Client
    assert Client is not None

def test_authenticate():
    """Can we authenticate with API key?"""
    client = Client(api_key=os.getenv("EDISON_API_KEY"))
    assert client.is_authenticated()

def test_basic_query():
    """Can we make a simple API call?"""
    client = Client(api_key=os.getenv("EDISON_API_KEY"))
    response = client.ping()  # or minimal health check
    assert response.status == "ok"
```

**Expected:** All fail initially (no client code written)

---

## Phase 1: Job Type Smoke Tests (30 min)

### Test Suite
```python
def test_literature_job_callable():
    """LITERATURE job type can be invoked"""
    client = Client(api_key=os.getenv("EDISON_API_KEY"))
    job = client.submit_job(
        job_type=JobNames.LITERATURE,
        query="What is CRISPR?"
    )
    assert job.job_id is not None

def test_analysis_job_callable():
    """ANALYSIS job type can be invoked"""
    # Similar pattern - expect failure until implemented

def test_precedent_job_callable():
    """PRECEDENT job type can be invoked"""
    # Similar pattern

def test_molecules_job_callable():
    """MOLECULES job type can be invoked"""
    # Similar pattern

def test_kosmos_job_callable():
    """Generic Kosmos job can be invoked"""
    # Similar pattern
```

**Expected:** All fail initially (no job submission code written)

---

## Phase 2: Benchmark Experiments (2 hours)

### Experiment 1: Cancer Genomics (LITERATURE)

**Ground Truth:**
- Known KRAS-mutant PDAC targets: SHP2, SOS1, MRTX1133, MRTX849
- Known resistance mechanisms: KRAS G12D/V bypass, MEK reactivation

**Test:**
```python
def test_cancer_genomics_identifies_known_targets():
    """Kosmos identifies documented KRAS targets"""
    result = run_literature_query("cancer_genomics")

    known_targets = ["SHP2", "SOS1", "MRTX1133", "MRTX849"]
    identified = extract_targets_from_result(result)

    # Should identify at least 75% of known targets
    overlap = len(set(known_targets) & set(identified))
    assert overlap >= 3, f"Only found {overlap}/4 known targets"

    # Should have ≥20 citations
    assert len(result.citations) >= 20

    # Spot-check 5 random citations exist
    sample_citations = random.sample(result.citations, 5)
    for citation in sample_citations:
        assert verify_citation_exists(citation), f"Fabricated: {citation}"
```

**Metrics:**
- Target recall: % of known targets identified
- Citation count: Total primary sources
- Citation validity: % of spot-checked citations that exist

---

### Experiment 2: Immunology (PRECEDENT)

**Ground Truth:**
- BioNTech BNT111: NCT02410733 (melanoma, personalized neoantigen)
- Moderna mRNA-4157: NCT03313778 (solid tumors, neoantigen)
- Gritstone SLATE: NCT03639714 (NSCLC, neoantigen)

**Test:**
```python
def test_immunology_finds_clinical_trials():
    """Precedent query identifies actual clinical trials"""
    result = run_precedent_query("immunology_vaccines")

    expected_trials = ["NCT02410733", "NCT03313778", "NCT03639714"]
    found_trials = extract_trial_ids(result)

    # Should find at least 2/3 trials
    overlap = len(set(expected_trials) & set(found_trials))
    assert overlap >= 2, f"Only found {overlap}/3 known trials"

    # Should correctly state "Yes" to precedent question
    assert result.precedent_exists == True

    # Should include outcome data
    assert result.clinical_outcomes is not None
```

**Metrics:**
- Trial recall: % of known trials identified
- Accuracy: Correct yes/no precedent answer
- Completeness: Includes outcome data

---

### Experiment 3: Systems Biology (ANALYSIS)

**Ground Truth:**
- E. coli heat shock dataset (GEO: GSE123456 - example)
- Known upregulated genes: dnaK, dnaJ, groEL, groES, htpG, clpB
- Expected pathway: σ32 (rpoH) heat shock response

**Test:**
```python
def test_systems_bio_identifies_canonical_genes():
    """Analysis identifies well-known heat shock genes"""
    result = run_analysis_query("systems_biology", dataset_path="input/ecoli_heatshock.csv")

    canonical_genes = ["dnaK", "dnaJ", "groEL", "groES", "htpG", "clpB"]
    identified_degs = extract_upregulated_genes(result)

    # Should identify at least 4/6 canonical genes
    overlap = len(set(canonical_genes) & set(identified_degs))
    assert overlap >= 4, f"Only found {overlap}/6 canonical heat shock genes"

    # Code should execute without errors
    assert result.notebook_executed == True
    assert result.execution_errors == []

    # Should generate figures
    assert len(result.figures) >= 2  # e.g., heatmap + volcano plot
```

**Metrics:**
- Gene recall: % of canonical genes identified
- Code execution: Success/failure
- Figure quality: Number and type of visualizations

---

### Experiment 4: Structural Biology (MOLECULES)

**Ground Truth:**
- Nirmatrelvir (Paxlovid): SMILES known, ADMET properties documented
- Required improvements: Oral bioavailability (F%), solubility (μg/mL)

**Test:**
```python
def test_structural_bio_designs_valid_molecules():
    """Phoenix generates chemically feasible Mpro inhibitors"""
    result = run_molecules_query("structural_biology")

    # Should propose 3 molecules
    assert len(result.proposed_molecules) == 3

    # Each should have valid SMILES
    for mol in result.proposed_molecules:
        assert is_valid_smiles(mol.smiles), f"Invalid SMILES: {mol.smiles}"

    # Should have ADMET predictions
    for mol in result.proposed_molecules:
        assert mol.admet_properties is not None
        assert "solubility" in mol.admet_properties
        assert "oral_bioavailability" in mol.admet_properties

    # At least 1 molecule should show improvement over nirmatrelvir
    baseline_solubility = get_nirmatrelvir_solubility()
    improved = [m for m in result.proposed_molecules
                if m.admet_properties["solubility"] > baseline_solubility]
    assert len(improved) >= 1, "No molecules show improved solubility"
```

**Metrics:**
- Chemical validity: % of molecules with valid SMILES
- Property coverage: % with complete ADMET predictions
- Improvement: % showing better properties than baseline

---

### Experiment 5: Neuroscience (LITERATURE)

**Ground Truth:**
- Known mechanisms: α-synuclein propagation via vagus nerve, LPS from gut, neuroinflammation
- Known therapeutics: GLP-1 agonists, probiotics, fecal transplant (preclinical)

**Test:**
```python
def test_neuroscience_identifies_mechanisms():
    """Literature synthesis finds established pathways"""
    result = run_literature_query("neuroscience_microbiome")

    known_mechanisms = ["alpha-synuclein", "vagus nerve", "LPS", "neuroinflammation"]
    identified_mechanisms = extract_mechanisms(result.content)

    # Should identify at least 3/4 mechanisms
    overlap = len(set(known_mechanisms) & set(identified_mechanisms))
    assert overlap >= 3, f"Only found {overlap}/4 known mechanisms"

    # Should rank intervention feasibility
    assert result.ranked_interventions is not None
    assert len(result.ranked_interventions) >= 3

    # Citations should include primary research
    primary_sources = [c for c in result.citations if c.is_primary_research]
    assert len(primary_sources) >= 15
```

**Metrics:**
- Mechanism recall: % of known pathways identified
- Ranking quality: Feasibility rankings present and justified
- Citation type: % primary research vs. reviews

---

## Evaluation Automation

### Per-Experiment Report Generation
```python
def generate_experiment_report(experiment_name, result, ground_truth):
    """Auto-generate markdown report with metrics"""
    report = {
        "experiment": experiment_name,
        "timestamp": datetime.now().isoformat(),
        "metrics": calculate_metrics(result, ground_truth),
        "citations_validated": validate_citations_sample(result.citations, n=5),
        "raw_output": result.to_dict(),
        "passed_tests": run_test_suite(experiment_name),
    }
    write_report(f"output/{experiment_name}_report.md", report)
```

### Aggregate Dashboard
- Overall pass rate (% tests passing)
- Per-job-type performance
- Citation accuracy across all experiments
- Time per experiment
- Cost per experiment ($200/run)

---

## Success Criteria

**Minimum Viable:**
- All Phase 0/1 tests pass
- 3/5 benchmark experiments pass ≥75% of assertions
- Zero fabricated citations in spot-checks

**Ideal:**
- All benchmark experiments pass 100% of assertions
- Execution time <2 hours total
- Expert reviewers rate outputs ≥4/5 for proposal relevance
