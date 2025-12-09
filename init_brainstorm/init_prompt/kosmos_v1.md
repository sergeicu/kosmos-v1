# Kosmos Testing PRD - Initial Prompt

## Context

**Tool:** Kosmos by Edison Scientific
**Access:** https://edisonscientific.com/articles/announcing-kosmos

**Grant:** Schmidt Sciences RCT (Randomized Control Trial)
**Objective:** Test computational biologists (control vs trial groups) using Kosmos for grant proposal generation

## Available Kosmos Job Types

### 1. JobNames.LITERATURE
Ask questions of scientific data sources with high-accuracy, cited responses. Built with PaperQA3.

**Suggested queries:**
- What are some likely mechanisms by which mutations near the HTRA1 locus in humans might be causal for age-related macular degeneration?
- What factors limit the wavelengths of light detectable by mammalian eyes?
- How might you capture electron transfer effects using classical force fields for molecular dynamics simulations of protein-protein interactions?

**Kosmos-specific queries:**
- Mechanism of entorhinal cortex vulnerability in aging
- Thermal annealing humidity as critical determinant for perovskite solar-cell performance
- Cis-regulation of SSR1 by a protective GWAS variant in Type 2 Diabetes in humans

### 2. JobNames.ANALYSIS
Turn biological datasets into detailed analyses answering research questions.

**Guide:** https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/edison_analysis_tutorial

### 3. JobNames.PRECEDENT
Query if anyone has ever done something in science. Can search clinicaltrials.gov database.

**Guide:** https://edisonscientific.gitbook.io/edison-cookbook/paperqa/docs/tutorials/querying_with_clinical_trials

**Suggested queries:**
- Has anyone developed efficient non CRISPR methods for modifying DNA?
- Has anyone studied using a RAG system to help make better diagnoses for patients?
- Has anyone ever made an all-atom autoencoder for proteins?

### 4. JobNames.MOLECULES
New iteration of ChemCrow (Phoenix) using cheminformatics tools. Good for synthesis planning and designing new molecules.

**Guide:** https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/phoenix_guidelines

**Suggested queries:**
- Propose a viable retrosynthesis route to produce the molecule OB(O)c1cc(Cl)ccc1F starting from purchasable precursors. Also give me an estimated total price for the reactants and search the literature for reaction yield of each step.
- Design an alternative small molecule to Lipitor that inhibits HMG-CoA reductase but has improved solubility through a more hydrophilic design. Compare the drug-likeness properties of your proposed drug with Lipitor.
- Research this molecule and then give three proposed modifications to increase its microsomal stability CC1=CC2=C(C=CC(=C2)C(=O)N(CC3=NC=C(C=C3)C(F)(F)F)[C@H](C)C4=NC=CC=N4)N=C1N. Compare the resulting stabilities.

## Kosmos Guidelines

**Source:** https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/kosmos_guidelines

### Best Practices

1. **Clear, Feasible Research Objective** - Single, well-defined question requiring iterative hypothesis testing. Should take weeks/months for an expert, not answerable from a few papers.

2. **Provide Sufficient Scientific Context** - Phrase as you would to an experienced colleague joining your team. Include experimental design choices, field-specific assumptions, non-obvious protocols.

3. **Well-Documented Data Description** - Column names should be intuitive or documented. Domain expert should understand without clarification.

4. **Supply Complex, High-Dimensional Data** - Works best with scRNA-seq, proteomics, environmental parameters across multiple samples/timepoints. Can handle up to 5GB uncompressed.

5. **Use Processed, High-Quality Data** - Most powerful with processed data. Avoid raw sequencing files or unannotated imaging data.

6. **Iterate and Refine** - Start with familiar datasets, progressively refine. Trial and error builds intuition.

## Grant Excerpt - RCT Summary

**Funding Source:** Schmidt Sciences pilot grant

**Objective:** Run, design, and de-risk a larger RCT measuring causal impact of AI on scientific discovery process.

**Pilot Goals:**
1. Validate tasks and outcome measures
2. Refine recruitment and compliance procedures
3. Produce credible power estimates for larger RCT

### Study Design

**Participants:** Early-career scientists developing short research projects across multiple scientific fields

**Treatment Group:**
- Access to FutureHouse AI tools (Crow, Falcon, Phoenix, Owl, Finch, Robin, Kosmos)
- Training on standardized technology stack
- Uncapped platform access

**Control Group:**
- Placebo intervention (general scientific research training)
- Q&A session with postdoc/PI from leading institution
- No AI tool access
- No knowledge that treatment group receives AI training

**Monitoring:** Digital logs, potential screen streaming (Loom, Twitch), digital scientific notebooks

**Compliance:** Direct employment model ensures high adherence to assigned conditions

### Task One: Research Proposal Generation

**Timeline:** 2 weeks per proposal

**Process:**
1. Crowdsource research topics from participants (NIH-style RFP)
2. Review and cluster ideas into subfields
3. Assign topics to relevant participants
4. Participants develop detailed research proposals requiring:
   - Background literature review
   - Hypothesis generation
   - Concrete experimental protocol design
5. Independent expert peer review (NIH study section style)

**Evaluation Dimensions:**
- Novelty
- Feasibility
- Perceived risk
- Potential scientific value

**Scientific Rationale:**
- Tests AI impact on early-stage discovery: knowledge synthesis, literature review, creative hypothesis generation, idea evaluation, experimental design
- Builds on authentic, real-world problems identified by scientists
- Even modest quality gains (5%) translate to less waste, greater efficiency, higher ROI

**Constraints:**
- Cannot directly implement all proposals due to financial/logistical limits
- Focus on measuring AI's ability to enhance proposal quality and experimental design

### Methodological Innovations

**Advantages:**
1. Direct compensation enables rich, granular data collection
2. Screen streaming decomposes where AI helps in research process
3. Digital notebooks track research decisions in real-time
4. High experimental compliance through employment structure
5. Continuous monitoring prevents treatment contamination

**Recruitment Strategy:**
- Frame as "investigating scientific discovery process" (not explicitly AI-focused)
- Reduces selection bias toward AI-enthusiastic participants
- Leverage Harvard/Berkeley relationships for network dissemination
- Target computational biology and chemistry fields for pilot

**Geographic Diversity:**
- Recruit from India and United States
- Examine if AI democratizes science or perpetuates inequalities
- Address research productivity distribution disparities

### Research Contributions

1. **Technology Impact Literature** - First comprehensive RCT on AI provision to large cohort of scientists
2. **Global Scientific Equity** - Cross-country analysis (India/US) of AI's democratization potential
3. **Tool Development Partnership** - Direct collaboration with FutureHouse to refine AI tools based on usage data
4. **AI Adoption Patterns** - Process-level data on how scientists use (or don't use) AI tools

## Test Requirements

**Time Constraint:** 2 hours total for testing
**Fields:** 3-5 computational biology fields
**Task Variety:** Each field tests different job type
**Criteria:** Dead simple yet very coherent experiments
**Relevance:** Must align with grant's research proposal generation focus
