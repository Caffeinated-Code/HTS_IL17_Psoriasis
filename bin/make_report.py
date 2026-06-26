#!/usr/bin/env python3
import csv
import html
import json
import sys
from datetime import datetime, timezone


rankings, evidence_md, html_out, provenance_out = sys.argv[1:5]
with open(rankings, newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
with open(evidence_md) as handle:
    evidence = handle.read()

table_rows = "\n".join(
    "<tr>"
    + "".join(f"<td>{html.escape(row[col])}</td>" for col in ["rank", "gene_symbol", "rank_score", "screen_qc_call", "top_cell_type", "limitations"])
    + "</tr>"
    for row in rows
)

doc = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>HTS_IL17_Psoriasis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; line-height: 1.5; color: #1f2937; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.45rem; text-align: left; vertical-align: top; }}
    th {{ background: #eef2f7; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; }}
    .note {{ background: #fff7ed; border-left: 4px solid #f97316; padding: 0.8rem; }}
  </style>
</head>
<body>
  <h1>HTS_IL17_Psoriasis Report</h1>
  <p class=\"note\">This report is generated from toy public-data-shaped demo tables. It demonstrates workflow structure, scoring, provenance, and evidence summarization.</p>
  <h2>Candidate Ranking</h2>
  <table>
    <thead><tr><th>Rank</th><th>Gene</th><th>Score</th><th>Screen QC</th><th>Top Cell Type</th><th>Limitations</th></tr></thead>
    <tbody>{table_rows}</tbody>
  </table>
  <h2>Evidence Cards</h2>
  <pre>{html.escape(evidence)}</pre>
</body>
</html>
"""
with open(html_out, "w") as out:
    out.write(doc)

provenance = {
    "project": "HTS_IL17_Psoriasis",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "mode": "toy_demo",
    "inputs": [
        "PubChem AID2604/AID2546-shaped demo data",
        "GSE54456-shaped demo data",
        "PXD021673-shaped demo data",
        "GSE162183-shaped demo data",
        "ESM-2/AlphaFoldDB-shaped demo features",
    ],
    "claim_guardrails": [
        "No clinical efficacy claims",
        "No company-specific claims",
        "Structure and LLM outputs are hypothesis-generating",
    ],
}
with open(provenance_out, "w") as out:
    json.dump(provenance, out, indent=2)
