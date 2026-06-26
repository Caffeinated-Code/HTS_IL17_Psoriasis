# Project Plan: HTS_IL17_Psoriasis

## Objective

Build a FAIR, locally runnable, AWS-adaptable Nextflow workflow and Streamlit app that integrates public HTS/qHTS-style assay data, psoriasis disease omics, proteomics, protein AI features, optional structure prediction evidence, and grounded LLM summaries.

The project should be reviewed as a staff-scientist-level portfolio artifact: scientifically useful, transparent about limitations, and structured so it could be extended to real internal screening data.

## Scientific Question

Which Th17/IL-17 psoriasis pathway candidates are most compelling when ranked by:

- HTS-style activity and counterscreen selectivity
- psoriasis disease expression evidence
- protein-level validation
- disease-relevant cell-type context
- protein AI model features
- optional AlphaFold/ESMFold structure confidence
- transparent LLM evidence summaries

## Implementation Phases

### Phase 1: Local Demo

- Use bundled toy datasets with public-data-shaped columns.
- Run `nextflow run main.nf -profile test`.
- Generate tables, evidence cards, report, and app data.
- Launch `streamlit run app/streamlit_app.py`.

### Phase 2: Public Data Expansion

- Add real PubChem PUG-REST retrieval for AID 2604 and AID 2546.
- Add ChEMBL API retrieval for RORC/IL-17 pathway assay records.
- Add processed GSE54456 import and DESeq2-style differential expression.
- Add PRIDE/PXD021673 processed protein quantification import.
- Add GSE162183 processed marker/cell-type summaries.

### Phase 3: Protein AI And Structure

- Add ESM-2, ProtBERT, or ProtTrans embedding generation for top candidates.
- Cache embeddings with accession, model name, and model version.
- Add AlphaFold DB lookup or optional ESMFold prediction for top candidates only.
- Keep GPU and large model calls optional.

### Phase 4: LLM Evidence Summaries

- Add a grounded summarization module that consumes workflow tables only.
- Require accession and table citations in every evidence card.
- Emit limitations and next-experiment suggestions.
- Allow local template mode when no LLM API key is available.

## Scoring Model

The first implementation uses a transparent weighted score:

| Component | Weight | Rationale |
| --- | ---: | --- |
| HTS activity | 0.20 | Captures screen signal |
| Counterscreen selectivity | 0.15 | Penalizes assay artifacts |
| Disease RNA evidence | 0.20 | Prioritizes psoriasis-relevant expression |
| Proteomics support | 0.15 | Adds protein-level validation |
| Cell-type relevance | 0.10 | Connects target to skin/immune cell biology |
| Protein AI feature score | 0.10 | Adds sequence/model-derived context |
| Structure confidence | 0.10 | Adds structural plausibility when available |

This should stay configurable in future versions.

## Actionable Biological Insights To Surface

- Does the candidate align with Th17/IL-17 biology, keratinocyte activation, cytokine signaling, or inflammatory skin proteomics?
- Is the candidate supported at both RNA and protein levels?
- Is the signal specific to disease-relevant cell types, or broadly expressed?
- Does the HTS signal survive counterscreen filtering?
- Is structure evidence high-confidence enough to support follow-up modeling?
- What validation experiment would reduce uncertainty fastest?

## Critical Review Notes

- The HTS data are pathway-proximal small-molecule assays, not peptide screens.
- ROR gamma is upstream of IL-17 biology; this supports relevance but not direct IL-17 binding.
- RNA-protein concordance can be imperfect; discordance should be flagged, not hidden.
- Protein language model embeddings are features, not explanations by themselves.
- Structure prediction confidence is not interaction validation.
- LLM output must be evidence-grounded and citation-backed.

## Things To Do

- Replace toy tables with full public dataset downloads.
- Add raw FASTQ mode for transcriptomics as an optional cloud workflow.
- Add richer cheminformatics for PubChem compounds.
- Add peptide-specific public assay data if a suitable source is found.
- Add model-card-style documentation for protein AI and LLM components.
- Add CI using `nextflow run main.nf -profile test`.
- Add screenshots after the app is visually reviewed.

