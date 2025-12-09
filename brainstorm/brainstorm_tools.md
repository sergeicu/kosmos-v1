# Tools Assessment - Edison Scientific Platform

## Available Kosmos Job Types

### 1. LITERATURE (PaperQA3)
**Purpose:** High-accuracy, cited responses from scientific literature
**Strengths:**
- ~1500 papers analyzed per run
- Full citation traceability
- 79.4% accuracy (documented)
**Limitations:**
- Limited to published literature (no preprints confirmed?)
- Time window unknown (last update?)

### 2. ANALYSIS
**Purpose:** Turn biological datasets into detailed analyses
**Strengths:**
- Python/R code generation
- External tool integration (web, gene DBs)
- 3-10 min execution typical
**Limitations:**
- Requires processed, high-quality data
- 5GB uncompressed limit
- No raw sequencing/imaging support

### 3. PRECEDENT
**Purpose:** Query if research has been done before
**Strengths:**
- ClinicalTrials.gov integration
- Binary answers (yes/no + evidence)
**Limitations:**
- Search scope unclear (PubMed? bioRxiv?)
- May miss unpublished work

### 4. MOLECULES (Phoenix/ChemCrow)
**Purpose:** Cheminformatics and synthesis planning
**Strengths:**
- ADMET predictions
- Retrosynthesis routes
- Database search (ChEMBL)
**Limitations:**
- Computational only (no experimental validation)
- Synthetic accessibility scores are estimates

## Testing Stack

### Phase 0: API Testing
- **Tool:** Edison Python SDK
- **Auth:** API key from environment/config
- **Validation:** Successful connection + basic query

### Phase 1: Smoke Tests
- **Tool:** Pytest for test harness
- **Pattern:** Call each job type, expect failure/success signal
- **TDD:** Write failing tests first

### Phase 2: Benchmarking
- **Ground Truth Sources:**
  - Known publications (manual curation)
  - Public datasets with documented results
  - Clinical trial registries
  - Chemical databases (PubChem, ChEMBL)
- **Evaluation:** Automated comparison scripts

## Infrastructure Requirements

### Parallel Execution
- 5 separate Claude Code instances
- Shared task definition format (Markdown)
- Isolated output directories per task

### Data Management
- Input: Public datasets (GEO, ArrayExpress)
- Output: Structured reports (JSON + Markdown)
- Logs: Timestamped execution traces

### Quality Metrics
- Automated: Citation validation, code execution success
- Manual: Expert review of scientific quality (1-5 Likert scale)
