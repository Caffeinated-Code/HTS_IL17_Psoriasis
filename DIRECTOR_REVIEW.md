# Director Review: HTS_IL17_Psoriasis

## Executive Assessment

This is a credible staff-scientist portfolio project because it connects screening data, disease biology, proteomics, protein AI, structure context, FAIR workflow design, and an app-facing interpretation layer. The strongest aspect is not the toy ranking itself; it is the architecture for turning heterogeneous discovery evidence into a transparent decision record.

The project should keep emphasizing one point clearly: this is a reusable workflow pattern. Psoriasis / IL-17 is the demo case.

## What Is Strong

- The project includes an HTS-like evidence layer rather than only omics.
- The scoring model is transparent and inspectable.
- The LLM module is appropriately grounded in workflow outputs.
- The documentation explains complex topics for mixed computational and biology audiences.
- The app makes the output reviewable by non-pipeline users.
- The Nextflow workflow has local and AWS-oriented profiles.

## Scientific Limitations To State Clearly

- PubChem ROR gamma qHTS is pathway-proximal. It supports Th17 / IL-17 biology but is not a direct IL-17 peptide assay.
- The current demo data are toy, candidate-level summaries shaped like public datasets.
- IL17A ranking highly is biologically intuitive, but the demo assay evidence for IL17A is contextual rather than direct.
- RORC ranking highly is assay-supported, but protein-level validation is weaker in the demo and should be flagged.
- TNF is a broad inflammatory node; a high disease/proteomics signal does not make it a specific IL-17-pathway candidate.
- Protein language model and structure scores are hypothesis-generating features, not validated predictors.

## Actionable Biological Insights

- **IL17A** is the strongest biology-positive control: it should rank high because disease expression, proteomics, and T-cell context align. The next validation should test whether candidate perturbations reduce IL-17-driven keratinocyte inflammatory outputs.
- **RORC** is the strongest screening-positive control: it should rank high from qHTS/counterscreen evidence but remain caveated because it is upstream and protein evidence is weaker. The next validation should confirm ROR gamma pathway modulation and check specificity.
- **IL23R** is a translationally useful intermediate candidate: it links upstream immune signaling to Th17 maintenance and should be evaluated for cell-type specificity.
- **STAT3** is mechanistically relevant but broad. Treat it as a pathway node requiring selectivity checks, not a clean target nomination.
- **TNF** should demonstrate the value of counterscreens and specificity penalties: disease evidence can be strong while screen selectivity is poor.

## Sequential Improvement Plan

### v0.2 - Replace Toy Tables With Public Retrieval

- Implement PubChem PUG-REST retrieval for AID 2604 and AID 2546.
- Add ChEMBL API retrieval for RORC/IL-17 pathway assay context.
- Store raw downloads under a user-specified cache path, not in git.
- Record checksums and retrieval dates in provenance.

### v0.3 - Real Disease Omics

- Import processed GSE54456 expression/count data.
- Add differential expression with a documented contrast.
- Add pathway enrichment for IL-17 signaling, cytokine signaling, keratinocyte activation, and Th17 differentiation.
- Add an independent validation dataset before expanding biological claims.

### v0.4 - Proteomics And Single-Cell Context

- Import processed PXD021673 protein quantification tables.
- Add RNA/protein concordance flags.
- Import processed GSE162183 cell-type markers or pseudobulk summaries.
- Add a warning when a candidate is broadly expressed rather than cell-type enriched.

### v0.5 - Protein AI And Structure

- Add real UniProt sequence retrieval.
- Add optional ESM-2 or ProtBERT embeddings with cached model metadata.
- Add AlphaFold DB lookup for candidate proteins.
- Keep ESMFold or heavier structure prediction optional and top-candidate-only.

### v0.6 - Evidence-Grounded LLM Mode

- Replace deterministic evidence-card templates with an optional RAG/LLM backend.
- Require all generated sentences to cite workflow table IDs or accessions.
- Add a validation test that rejects evidence cards with missing citations.
- Keep deterministic template mode as the default for reproducibility.

## Staff Scientist Bar For The Next Version

The next version should answer this review question:

> If I only had enough budget to validate two candidates, which two should I choose, what experiment should I run first, and what evidence would make me stop?

The current demo begins to answer that by nominating IL17A and RORC for different reasons: IL17A as disease-biology aligned, RORC as screen-supported and pathway-proximal. The next version should make that tradeoff quantitative and explicit.

