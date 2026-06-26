#!/usr/bin/env python3
import csv
import sys


rankings, md_out, tsv_out = sys.argv[1:4]
with open(rankings, newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

with open(md_out, "w") as md, open(tsv_out, "w", newline="") as tsv:
    fields = ["rank", "gene_symbol", "summary", "limitations", "next_experiment", "citations"]
    writer = csv.DictWriter(tsv, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    md.write("# Grounded LLM-Style Evidence Cards\n\n")
    md.write("These cards use a deterministic template that mimics the desired LLM/RAG output. A production LLM module should cite the same workflow tables and accessions.\n\n")
    for row in rows:
        summary = (
            f"{row['gene_symbol']} ranks #{row['rank']} with a transparent score of {row['rank_score']}. "
            f"The candidate combines {row['screen_qc_call']} screening evidence, disease score {row['disease_score']}, "
            f"proteomics score {row['proteomics_score']}, and {row['top_cell_type']} cell-type context. "
            "This is a hypothesis-generating prioritization result, not proof of therapeutic efficacy."
        )
        if row["gene_symbol"] in {"IL17A", "IL23R", "RORC"}:
            next_experiment = "Validate pathway modulation in a psoriasis-relevant keratinocyte/immune co-culture assay with orthogonal protein readouts."
        elif row["gene_symbol"] == "STAT3":
            next_experiment = "Test specificity of pathway modulation and separate broad signaling effects from disease-selective biology."
        else:
            next_experiment = "Run focused counterscreens to distinguish broad inflammation from specific IL-17 pathway modulation."
        writer.writerow({
            "rank": row["rank"],
            "gene_symbol": row["gene_symbol"],
            "summary": summary,
            "limitations": row["limitations"],
            "next_experiment": next_experiment,
            "citations": row["dataset_citations"],
        })
        md.write(f"## {row['rank']}. {row['gene_symbol']} - {row['protein_name']}\n\n")
        md.write(f"**Summary:** {summary}\n\n")
        md.write(f"**Limitations:** {row['limitations']}\n\n")
        md.write(f"**Suggested next validation:** {next_experiment}\n\n")
        md.write(f"**Citations:** {row['dataset_citations']}\n\n")
