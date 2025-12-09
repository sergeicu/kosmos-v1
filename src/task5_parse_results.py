#!/usr/bin/env python3
"""
Parse the rich Kosmos response for Task 5
"""

import json
import re
from pathlib import Path


def parse_kosmos_response():
    """Parse the detailed Kosmos response"""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output" / "task5_results"

    # Load raw results
    with open(output_dir / "kosmos_raw_output.json") as f:
        raw_data = json.load(f)

    answer = raw_data["results"]["answer"]

    parsed = {
        "identified_mechanisms": [],
        "circuit_level_details": [],
        "ranked_interventions": [],
        "citations": [],
        "additional_info": {
            "intervention_signals": [],
            "mechanism_intervention_mapping": {},
            "synthesis": ""
        }
    }

    # Extract mechanisms (from the numbered list in the response)
    mech_pattern = r'\d\)\s*(.*?)(?=\n\d\)|\n\n|$)'
    mechanisms = re.findall(mech_pattern, answer, re.DOTALL)

    for mech in mechanisms:
        # Clean up mechanism text
        mech_clean = mech.strip().replace('\n', ' ')
        if len(mech_clean) > 20:  # Filter out short fragments
            parsed["identified_mechanisms"].append(mech_clean[:300])  # Limit length

    # Extract intervention ranking
    # Look for the numbered ranking section
    ranking_pattern = r'Ranking potential interventions by current feasibility.*?(?=\n\n|Synthesis)'
    ranking_section = re.search(ranking_pattern, answer, re.DOTALL)

    if ranking_section:
        # Extract numbered interventions
        intervention_pattern = r'\d\)\s*(.*?)\.(?=.*\d\)|$)'
        interventions = re.findall(intervention_pattern, ranking_section.group(0), re.DOTALL)

        for intervention in interventions:
            # Extract first sentence as intervention name
            intervention_clean = intervention.strip()
            if '.' in intervention_clean:
                first_sentence = intervention_clean.split('.')[0]
            else:
                first_sentence = intervention_clean[:100]
            parsed["ranked_interventions"].append(first_sentence.strip())

    # Extract citations from References section
    # The DOIs are in the formatted_answer field
    formatted_answer = raw_data["results"]["formatted_answer"]

    # Extract all DOI patterns
    doi_patterns = [
        r'https://doi\.org/10\.\d+/[^\s,\)]+',
        r'10\.\d+/[a-zA-Z0-9\.\-_/]+'
    ]

    all_dois = set()
    for pattern in doi_patterns:
        matches = re.findall(pattern, formatted_answer)
        all_dois.update(matches)

    # Clean up DOIs
    clean_dois = []
    for doi in all_dois:
        if doi.startswith('https://'):
            clean_dois.append(doi)
        elif '.' in doi and len(doi) > 10:  # Basic validation
            clean_dois.append(f"https://doi.org/{doi}")

    parsed["citations"] = clean_dois[:50]  # Limit to 50 most recent

    # Extract circuit-level details
    circuit_keywords = ["vagus", "enteric", "ENS", "vagal", "sympathetic", "nodose", "DMV"]
    sentences = answer.split('. ')
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in circuit_keywords):
            if len(sentence.strip()) > 30:
                parsed["circuit_level_details"].append(sentence.strip()[:200])

    # Extract synthesis/perspective
    synthesis_pattern = r'Synthesis and perspective.*?(?=Key limitations|$)'
    synthesis_match = re.search(synthesis_pattern, answer, re.DOTALL)
    if synthesis_match:
        parsed["additional_info"]["synthesis"] = synthesis_match.group(0).strip()

    # Save parsed results
    with open(output_dir / "parsed_results.json", "w") as f:
        json.dump(parsed, f, indent=2)

    print(f"Parsed {len(parsed['identified_mechanisms'])} mechanisms")
    print(f"Parsed {len(parsed['ranked_interventions'])} interventions")
    print(f"Parsed {len(parsed['citations'])} citations")
    print(f"Results saved to {output_dir / 'parsed_results.json'}")


if __name__ == "__main__":
    parse_kosmos_response()