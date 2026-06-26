# Analysis Walkthrough

This walkthrough explains how to read the `HTS_IL17_Psoriasis` demo like a discovery scientist reviewing a screening-to-biology prioritization workflow.

## 1. Start With The Scientific Question

The workflow asks:

> Which psoriasis / IL-17 pathway candidates remain interesting after combining screening-style evidence, disease omics, proteomics, cell-type context, protein AI features, and structural plausibility?

This is not designed to prove efficacy. It is designed to prioritize what deserves the next experiment.

## 2. Interpret The HTS Layer Carefully

The screening layer uses ROR gamma qHTS-style data as a public, pathway-proximal analog for Th17 / IL-17 biology. ROR gamma t is relevant because it regulates Th17 differentiation and IL-17 production.

The key distinction:

- **Supported claim:** this is a useful public screening-data analog for upstream Th17 biology.
- **Unsupported claim:** this is a direct IL-17 peptide screen.

That is why the dashboard includes a caveat. It is not meant to weaken the project; it shows scientific judgment.

## 3. Apply Counterscreen Logic

The screen QC module combines:

- primary assay activity
- counterscreen activity
- selectivity
- artifact flag

Candidates with strong primary activity but poor counterscreen behavior are penalized. In the demo, TNF has disease relevance but is flagged for artifact risk, which prevents it from ranking too highly.

## 4. Add Disease Transcriptomics

The disease omics layer asks whether the candidate is transcriptionally supported in psoriasis skin.

Strong disease RNA evidence helps prioritize candidates such as IL17A and IL23R because they align with psoriasis inflammatory biology.

## 5. Add Protein-Level Validation

Proteomics asks whether the disease signal is visible at the protein level.

This matters because RNA and protein signals can diverge. In the demo, RORC has strong screening support but weaker protein-level support, so it remains interesting but caveated.

## 6. Add Cell-Type Context

Single-cell context asks which cell populations carry the signal.

For psoriasis / IL-17 biology, T-cell context supports Th17 relevance, while keratinocyte context supports downstream inflammatory skin response. Broad expression can be useful biologically but less specific for target prioritization.

## 7. Add Protein AI And Structure Features

Protein language model features and structure confidence are included as contextual evidence.

They can help summarize protein family, sequence context, and structural interpretability. They do not prove mechanism, binding, or efficacy. The workflow treats them as supporting features, not as final answers.

## 8. Review The Integrated Ranking

The ranking is intentionally transparent:

| Evidence layer | Role in ranking |
| --- | --- |
| Screen QC | Is there screening-style activity and selectivity? |
| Disease RNA | Is the candidate disease-relevant in psoriasis tissue? |
| Proteomics | Is there protein-level support? |
| Cell context | Is the signal in relevant cells? |
| Protein AI | Does sequence/model context support interpretation? |
| Structure | Is the protein structurally interpretable? |

## 9. Read The Top Candidates Like A Reviewer

### IL17A

IL17A ranks first because the disease, proteomics, and T-cell context are aligned. In a real project, this is a biology-positive control: the workflow should recover it.

Actionable next step: validate IL-17 pathway modulation in a psoriasis-relevant keratinocyte / immune co-culture assay with orthogonal cytokine and protein readouts.

### RORC

RORC ranks highly because the screening layer is strongest. It is upstream of IL-17 biology, but the proteomics support is weaker in the demo.

Actionable next step: confirm ROR gamma pathway modulation and separate true pathway activity from transcriptional assay artifacts.

### IL23R

IL23R is a mechanistically coherent upstream immune candidate with disease and cell-context support.

Actionable next step: evaluate IL-23-driven Th17 response markers and compare with IL17A/RORC behavior.

### STAT3

STAT3 is relevant but broad. It should be treated as a pathway node requiring specificity checks.

Actionable next step: test whether perturbation selectively affects IL-17 biology or broadly suppresses signaling.

### TNF

TNF is intentionally useful as a cautionary example: strong inflammatory relevance does not overcome weak screening selectivity and artifact risk.

Actionable next step: run focused counterscreens and avoid over-prioritizing broad inflammatory nodes without specificity.

## 10. What The LLM Layer Does

The evidence-card module behaves like a grounded LLM/RAG summarizer. In this demo it uses deterministic templates, but the intended production behavior is:

- only summarize workflow-generated evidence
- cite dataset accessions and output tables
- separate evidence from hypothesis
- suggest the next validation experiment
- avoid unsupported biological claims

## 11. How To Explain The Project

A concise explanation:

> This project demonstrates a FAIR screening-to-biology workflow. It starts with public qHTS-style assay evidence around ROR gamma / Th17 biology, then layers in psoriasis transcriptomics, proteomics, single-cell context, protein AI features, structure confidence, and grounded evidence summaries. The result is a transparent ranking that helps decide which candidates deserve follow-up experiments, while clearly stating limitations.

