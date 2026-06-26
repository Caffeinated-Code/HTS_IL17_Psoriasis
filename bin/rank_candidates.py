#!/usr/bin/env python3
import argparse
import csv


WEIGHTS = {
    "screen_qc_score": 0.20,
    "selectivity_score": 0.15,
    "disease_score": 0.20,
    "proteomics_score": 0.15,
    "celltype_score": 0.10,
    "protein_ai_score": 0.10,
    "structure_confidence_score": 0.10,
}


def load_by_gene(path):
    with open(path, newline="") as handle:
        return {row["gene_symbol"]: row for row in csv.DictReader(handle, delimiter="\t")}


def f(row, key):
    try:
        return float(row.get(key, 0) or 0)
    except ValueError:
        return 0.0


parser = argparse.ArgumentParser()
parser.add_argument("--screen", required=True)
parser.add_argument("--disease", required=True)
parser.add_argument("--proteomics", required=True)
parser.add_argument("--singlecell", required=True)
parser.add_argument("--protein", required=True)
parser.add_argument("--structure", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

screen = load_by_gene(args.screen)
disease = load_by_gene(args.disease)
proteomics = load_by_gene(args.proteomics)
singlecell = load_by_gene(args.singlecell)
protein = load_by_gene(args.protein)
structure = load_by_gene(args.structure)

rows = []
for gene, s in screen.items():
    d = disease.get(gene, {})
    p = proteomics.get(gene, {})
    c = singlecell.get(gene, {})
    m = protein.get(gene, {})
    st = structure.get(gene, {})
    score = (
        WEIGHTS["screen_qc_score"] * f(s, "screen_qc_score")
        + WEIGHTS["selectivity_score"] * f(s, "selectivity_score")
        + WEIGHTS["disease_score"] * f(d, "disease_score")
        + WEIGHTS["proteomics_score"] * f(p, "proteomics_score")
        + WEIGHTS["celltype_score"] * f(c, "celltype_score")
        + WEIGHTS["protein_ai_score"] * f(m, "protein_ai_score")
        + WEIGHTS["structure_confidence_score"] * f(st, "structure_confidence_score")
    )
    limitation = []
    if s.get("artifact_flag", "").lower() == "true":
        limitation.append("counterscreen artifact risk")
    if f(p, "proteomics_score") < 0.55:
        limitation.append("weak protein-level support")
    if gene == "RORC":
        limitation.append("pathway-proximal qHTS, not direct IL-17 peptide screen")
    rows.append({
        "candidate_id": s["candidate_id"],
        "gene_symbol": gene,
        "protein_name": s["protein_name"],
        "rank_score": f"{score:.3f}",
        "screen_qc_score": s["screen_qc_score"],
        "screen_qc_call": s["screen_qc_call"],
        "selectivity_score": s["selectivity_score"],
        "disease_score": d.get("disease_score", "0"),
        "proteomics_score": p.get("proteomics_score", "0"),
        "celltype_score": c.get("celltype_score", "0"),
        "protein_ai_score": m.get("protein_ai_score", "0"),
        "structure_confidence_score": st.get("structure_confidence_score", "0"),
        "top_cell_type": c.get("top_cell_type", "unknown"),
        "dataset_citations": "; ".join(filter(None, [
            "PubChem AID2604/AID2546",
            d.get("dataset_accession"),
            p.get("dataset_accession"),
            c.get("dataset_accession"),
        ])),
        "biological_interpretation": " | ".join(filter(None, [
            s.get("hts_note"),
            d.get("disease_note"),
            p.get("proteomics_note"),
            c.get("celltype_note"),
            m.get("model_note"),
            st.get("structure_note"),
        ])),
        "limitations": "; ".join(limitation) if limitation else "No major limitation flagged beyond compact public example-data scope.",
    })

rows.sort(key=lambda row: float(row["rank_score"]), reverse=True)
for idx, row in enumerate(rows, start=1):
    row["rank"] = idx

fields = [
    "rank", "candidate_id", "gene_symbol", "protein_name", "rank_score",
    "screen_qc_score", "screen_qc_call", "selectivity_score", "disease_score",
    "proteomics_score", "celltype_score", "protein_ai_score",
    "structure_confidence_score", "top_cell_type", "dataset_citations",
    "biological_interpretation", "limitations",
]
with open(args.out, "w", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)
