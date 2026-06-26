from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
APP_DATA = ROOT / "results" / "app_data"
DEMO_DATA = ROOT / "demo_data"


def read_table(name, fallback=None):
    path = APP_DATA / name
    if not path.exists() and fallback:
        path = fallback
    if not path.exists():
        st.error(f"Missing table: {path}")
        st.stop()
    return pd.read_csv(path, sep="\t")


st.set_page_config(page_title="HTS_IL17_Psoriasis", layout="wide")

st.title("HTS_IL17_Psoriasis")
st.caption("Screening-to-biology prioritization demo with FAIR workflow outputs and grounded evidence summaries.")

rankings = read_table(
    "candidate_rankings.tsv",
    ROOT / "results" / "tables" / "candidate_rankings.tsv"
    if (ROOT / "results" / "tables" / "candidate_rankings.tsv").exists()
    else DEMO_DATA / "candidate_rankings.tsv",
)
cards = read_table("evidence_cards.tsv", DEMO_DATA / "evidence_cards.tsv")

st.warning(
    "Interpretation note: ROR gamma qHTS is pathway-proximal evidence for upstream Th17 / IL-17 biology, "
    "not a direct IL-17 peptide screen or efficacy model. "
    "Run `nextflow run main.nf -profile test` to regenerate the primary app tables."
)

with st.expander("Analysis walkthrough", expanded=True):
    st.markdown(
        """
1. Start with public qHTS-style screening evidence around ROR gamma / Th17 biology.
2. Penalize assay artifacts using counterscreen selectivity.
3. Add psoriasis transcriptomics to test disease relevance.
4. Add proteomics to check whether RNA-supported candidates have protein-level support.
5. Add single-cell context to localize the signal to relevant immune or skin-cell compartments.
6. Add protein AI and structure features as supporting interpretation layers.
7. Generate grounded evidence cards that explain the ranking, limitations, and next validation experiment.
"""
    )

score_cols = [
    "screen_qc_score",
    "selectivity_score",
    "disease_score",
    "proteomics_score",
    "celltype_score",
    "protein_ai_score",
    "structure_confidence_score",
]
for col in score_cols + ["rank_score"]:
    rankings[col] = pd.to_numeric(rankings[col], errors="coerce")

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Ranked Candidates")
    st.dataframe(
        rankings[
            [
                "rank",
                "gene_symbol",
                "protein_name",
                "rank_score",
                "screen_qc_call",
                "top_cell_type",
                "limitations",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("Transparent Score Breakdown")
    selected_gene = st.selectbox("Candidate", rankings["gene_symbol"].tolist())
    selected = rankings.loc[rankings["gene_symbol"] == selected_gene].iloc[0]
    score_frame = pd.DataFrame(
        {"component": score_cols, "score": [selected[col] for col in score_cols]}
    )
    fig = px.bar(score_frame, x="score", y="component", orientation="h", range_x=[0, 1])
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Evidence Card")
if not cards.empty:
    card = cards.loc[cards["gene_symbol"] == selected_gene].iloc[0]
    st.markdown(f"**Summary:** {card['summary']}")
    st.markdown(f"**Limitations:** {card['limitations']}")
    st.markdown(f"**Suggested next validation:** {card['next_experiment']}")
    st.markdown(f"**Citations:** {card['citations']}")
else:
    st.info("Run the Nextflow workflow to generate evidence cards.")

st.subheader("Biological Interpretation")
st.write(selected["biological_interpretation"])

st.subheader("Screening And Disease Evidence Map")
fig2 = px.scatter(
    rankings,
    x="screen_qc_score",
    y="disease_score",
    size="rank_score",
    color="gene_symbol",
    hover_data=["proteomics_score", "top_cell_type", "limitations"],
    range_x=[0, 1],
    range_y=[0, 1],
)
fig2.update_layout(height=420)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Director-Level Review Lens")
st.markdown(
    """
- Prioritize candidates supported by more than one evidence layer.
- Penalize counterscreen artifacts and broad inflammatory nodes when specificity is weak.
- Treat protein AI and structure features as context, not proof.
- Ask what validation experiment would reduce uncertainty fastest.
"""
)
