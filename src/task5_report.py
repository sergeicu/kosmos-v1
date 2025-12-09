#!/usr/bin/env python3
"""
Task 5 Report Generator
Creates a comprehensive markdown report for the neuroscience LITERATURE experiment
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_json(file_path):
    """Load JSON file safely"""
    try:
        with open(file_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {file_path}: {e}")
        return {}


def format_timestamp(iso_timestamp):
    """Format ISO timestamp for display"""
    if not iso_timestamp:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_timestamp


def generate_report():
    """Generate the Task 5 report"""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output" / "task5_results"
    input_dir = base_dir / "input"
    logs_dir = base_dir / "logs"

    # Load all data
    ground_truth = load_json(input_dir / "task5_ground_truth.json")
    raw_output = load_json(output_dir / "kosmos_raw_output.json")
    parsed = load_json(output_dir / "parsed_results.json")
    metrics = load_json(output_dir / "metrics.json")

    # Extract query
    query = """What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which mechanisms are most amenable to therapeutic intervention? Rank potential interventions by current feasibility (clinical readiness, mechanistic understanding, and safety profile)."""

    # Report header
    report = f"""# Task 5: Neuroscience - Results

## Execution Summary
- **Start time:** {format_timestamp(raw_output.get('collection_time', metrics.get('evaluation_timestamp')))}
- **End time:** {format_timestamp(metrics.get('evaluation_timestamp'))}
- **Duration:** ~15 minutes (Kosmos job) + 5 minutes (evaluation)
- **Cost:** $200

## Kosmos Query
```
{query}
```

## Ground Truth Comparison

### Mechanisms Identified
| Mechanism | Found by Kosmos | In Ground Truth | Evidence Strength |
|-----------|----------------|-----------------|-------------------|
"""

    # Check mechanisms
    identified_mechs = parsed.get("identified_mechanisms", [])
    if metrics and "mechanism_recall" in metrics:
        matched = metrics["mechanism_recall"].get("matched_mechanisms", [])
        all_mechs = [m["name"] for m in ground_truth.get("established_mechanisms", [])]

        for mech in ground_truth.get("established_mechanisms", []):
            found = "✓" if mech["name"].lower() in [m.lower() for m in matched] else "✗"
            report += f"| {mech['name']} | {found} | ✓ | {mech['evidence_strength']} |\n"

    # Additional mechanisms found by Kosmos
    if len(identified_mechs) > len(metrics.get("mechanism_recall", {}).get("matched_mechanisms", [])):
        report += "| Additional mechanisms | ✓ | ✗ | ... |\n"

    recall_pct = metrics.get("mechanism_recall", {}).get("percentage", 0)
    matched_count = len(metrics.get("mechanism_recall", {}).get("matched_mechanisms", []))
    total_count = metrics.get("mechanism_recall", {}).get("total_ground_truth", 0)

    report += f"""
**Mechanism Recall:** {recall_pct:.1f}% ({matched_count}/{total_count} established mechanisms found)

### Intervention Ranking

**Kosmos Ranking:**
"""

    kosmos_ranking = parsed.get("ranked_interventions", [])
    for i, intervention in enumerate(kosmos_ranking[:5], 1):
        if isinstance(intervention, str):
            report += f"{i}. {intervention}\n"
        elif isinstance(intervention, dict):
            name = intervention.get("intervention", intervention.get("name", str(intervention)))
            report += f"{i}. {name}\n"

    report += "\n**Expected Ranking (by feasibility):**\n"
    for i, intervention in enumerate(ground_truth.get("expected_ranking_order", []), 1):
        report += f"{i}. {intervention}\n"

    tau = metrics.get("intervention_ranking", {}).get("kendall_tau", 0)
    report += f"""
**Ranking Quality (Kendall's tau):** {tau:.2f} (target: ≥0.5)

**Analysis:**
{format_ranking_analysis(tau, metrics.get("intervention_ranking", {}))}

### Citations
- **Total citations:** {metrics.get("citation_metrics", {}).get("total_citations", 0)}
- **Primary research articles:** {metrics.get("citation_metrics", {}).get("primary_research_count", 0)} ({metrics.get("citation_metrics", {}).get("primary_research_percentage", 0):.0f}% of total, target: ≥60%)
- **Review articles:** {metrics.get("citation_metrics", {}).get("total_citations", 0) - metrics.get("citation_metrics", {}).get("primary_research_count", 0)}
"""

    # Key papers coverage
    if "key_papers_coverage" in metrics:
        coverage = metrics["key_papers_coverage"]["coverage"]
        report += "\n**Key Papers Coverage:**\n"
        report += "| DOI | Topic | Cited by Kosmos |\n"
        report += "|-----|-------|-----------------|\n"

        paper_topics = {
            "10.1002/ana.24448": "Vagal propagation",
            "10.1001/jamaneurol.2014.3865": "Vagotomy epidemiology",
            "10.1038/s41586-020-03186-4": "LPS inflammation",
            "10.1016/j.neuron.2020.01.033": "Microbiome-brain axis",
            "10.1038/s41531-020-00156-5": "SCFA depletion",
            "10.1016/j.cell.2015.09.016": "Neurotransmitter alterations"
        }

        for doi, cited in coverage.items():
            topic = paper_topics.get(doi, "Unknown")
            checkmark = "✓" if cited else "✗"
            report += f"| {doi} | {topic} | {checkmark} |\n"

    # Metrics table
    report += f"""
## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|"""

    if metrics:
        passes = metrics.get("passes", {})
        targets = metrics.get("targets", {})

        report += f"""
| Mechanism recall | ≥75% | {recall_pct:.1f}% | {'PASS' if passes.get('mechanism_recall') else 'FAIL'} |
| Ranking quality (τ) | ≥0.5 | {tau:.2f} | {'PASS' if passes.get('intervention_ranking') else 'FAIL'} |
| Citation count | ≥15 | {metrics.get('citation_metrics', {}).get('total_citations', 0)} | {'PASS' if passes.get('citation_count') else 'FAIL'} |
| Primary research ratio | ≥60% | {metrics.get('citation_metrics', {}).get('primary_research_percentage', 0):.0f}% | {'PASS' if passes.get('primary_research_ratio') else 'FAIL'} |"""

    report += f"""

## Overall Assessment
**{'PASS' if metrics.get('overall_pass') else 'FAIL'}**: based on {sum(metrics.get('passes', {}).values())}/4 metrics passing

## Cross-Domain Synthesis Quality
{assess_synthesis_quality(parsed, metrics)}

## Therapeutic Feasibility Assessment
{assess_feasibility_assessment(kosmos_ranking, metrics)}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../logs/task5_execution.log`

## Notes
{generate_notes(parsed, metrics)}
"""

    # Save report
    report_file = output_dir / "task5_report.md"
    with open(report_file, "w") as f:
        f.write(report)

    print(f"Report saved to: {report_file}")
    return report


def format_ranking_analysis(tau, ranking_metrics):
    """Format analysis of intervention ranking"""
    if tau >= 0.7:
        return ("Kosmos demonstrated excellent ranking quality, correctly prioritizing "
                "interventions with high clinical readiness and strong safety profiles.")
    elif tau >= 0.3:
        return ("Kosmos showed moderate ranking quality. Some interventions were "
                "correctly prioritized but the ordering could be improved.")
    else:
        return ("Kosmos struggled with ranking interventions by feasibility. The "
                "ordering does not align well with clinical readiness and safety considerations.")


def assess_synthesis_quality(parsed, metrics):
    """Assess cross-domain synthesis quality"""
    mechanisms = parsed.get("identified_mechanisms", [])

    if not mechanisms:
        return "Kosmos did not identify any mechanisms to analyze."

    synthesis_points = []

    # Check for circuit-level details
    has_circuit = any(keyword in str(mechanisms).lower()
                     for keyword in ["vagus", "enteric", "neural", "circuit", "pathway"])
    if has_circuit:
        synthesis_points.append("✓ Provided circuit-level details (neural pathways)")
    else:
        synthesis_points.append("✗ Lacked specific circuit-level details")

    # Check for cross-domain integration
    has_microbiome = any(keyword in str(mechanisms).lower()
                        for keyword in ["microbiome", "gut", "bacterial", "microbial"])
    has_neuro = any(keyword in str(mechanisms).lower()
                   for keyword in ["neuron", "brain", "neural", "dopamine"])

    if has_microbiome and has_neuro:
        synthesis_points.append("✓ Successfully integrated microbiology + neuroscience literature")
    else:
        synthesis_points.append("✗ Limited cross-domain integration")

    # Check for causation vs correlation
    has_causation = any(keyword in str(mechanisms).lower()
                       for keyword in ["caus", "mechanism", "propagation", "trigger"])
    if has_causation:
        synthesis_points.append("✓ Addressed causal relationships")
    else:
        synthesis_points.append("? May conflate correlation with causation")

    return "\n".join(synthesis_points)


def assess_feasibility_assessment(kosmos_ranking, metrics):
    """Assess therapeutic feasibility assessment"""
    if not kosmos_ranking:
        return "No intervention ranking provided by Kosmos."

    assessment_points = []

    # Check if GLP-1 agonists are prioritized (expected #1)
    glp1_found = any("glp" in str(item).lower() for item in kosmos_ranking)
    if glp1_found:
        assessment_points.append("✓ Recognized GLP-1 agonists (high clinical readiness)")
    else:
        assessment_points.append("✗ May have missed GLP-1 agonists")

    # Check for safety considerations
    has_safety = any(keyword in str(kosmos_ranking).lower()
                     for keyword in ["safety", "risk", "adverse", "profile"])
    if has_safety:
        assessment_points.append("✓ Considered safety profiles")
    else:
        assessment_points.append("? Safety considerations unclear")

    # Check for clinical trials
    has_trials = any(keyword in str(kosmos_ranking).lower()
                     for keyword in ["trial", "clinical", "phase", "nct"])
    if has_trials:
        assessment_points.append("✓ Referenced clinical trial evidence")
    else:
        assessment_points.append("? Clinical trial evidence unclear")

    return "\n".join(assessment_points)


def generate_notes(parsed, metrics):
    """Generate notes about the experiment"""
    notes = []

    # Note on mechanism identification
    identified_count = len(parsed.get("identified_mechanisms", []))
    expected_count = 4  # From ground truth

    if identified_count > expected_count:
        notes.append(f"Kosmos identified {identified_count} mechanisms, more than the {expected_count} established ones. "
                    "This may include novel mechanisms or broader interpretations.")
    elif identified_count < expected_count:
        notes.append(f"Kosmos only identified {identified_count} mechanisms, missing some established pathways.")

    # Note on citation quality
    primary_pct = metrics.get("citation_metrics", {}).get("primary_research_percentage", 0)
    if primary_pct < 60:
        notes.append(f"Primary research ratio ({primary_pct:.0f}%) below target. "
                    "Kosmos may rely more on review articles than primary research.")

    # Note on text parsing
    if "text_content" in parsed:
        notes.append("Results were provided as raw text rather than structured data. "
                    "Manual parsing may be required for full analysis.")

    return "\n".join(notes) if notes else "No specific issues identified."


if __name__ == "__main__":
    generate_report()