nextflow.enable.dsl = 2

params.outdir = params.outdir ?: 'results'
params.demo_data = params.demo_data ?: 'demo_data'

process FETCH_ASSAYS {
    tag 'fetch_assays'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path screen_file, stageAs: 'input_screen_assays.tsv'

    output:
    path 'screen_assays.tsv'

    script:
    """
    cp input_screen_assays.tsv screen_assays.tsv
    """
}

process SCREEN_QC {
    tag 'screen_qc'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path screen_file

    output:
    path 'screen_qc.tsv'

    script:
    """
    python3 "${projectDir}/bin/screen_qc.py" ${screen_file} screen_qc.tsv
    """
}

process DISEASE_OMICS {
    tag 'disease_omics'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path disease_file, stageAs: 'input_disease_omics.tsv'

    output:
    path 'disease_omics.tsv'

    script:
    """
    cp input_disease_omics.tsv disease_omics.tsv
    """
}

process PROTEOMICS_VALIDATE {
    tag 'proteomics_validate'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path proteomics_file, stageAs: 'input_proteomics_validation.tsv'

    output:
    path 'proteomics_validation.tsv'

    script:
    """
    cp input_proteomics_validation.tsv proteomics_validation.tsv
    """
}

process SINGLECELL_CONTEXT {
    tag 'singlecell_context'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path singlecell_file, stageAs: 'input_singlecell_context.tsv'

    output:
    path 'singlecell_context.tsv'

    script:
    """
    cp input_singlecell_context.tsv singlecell_context.tsv
    """
}

process PROTEIN_EMBEDDINGS {
    tag 'protein_embeddings'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path protein_file, stageAs: 'input_protein_features.tsv'

    output:
    path 'protein_features.tsv'

    script:
    """
    cp input_protein_features.tsv protein_features.tsv
    """
}

process STRUCTURE_FEATURES {
    tag 'structure_features'
    publishDir "${params.outdir}/tables", mode: 'copy'

    input:
    path structure_file, stageAs: 'input_structure_features.tsv'

    output:
    path 'structure_features.tsv'

    script:
    """
    cp input_structure_features.tsv structure_features.tsv
    """
}

process RANK_CANDIDATES {
    tag 'rank_candidates'
    publishDir "${params.outdir}/tables", mode: 'copy'
    publishDir "${params.outdir}/app_data", mode: 'copy', pattern: 'candidate_rankings.tsv'

    input:
    path screen_qc
    path disease
    path proteomics
    path singlecell
    path protein_features
    path structure_features

    output:
    path 'candidate_rankings.tsv'

    script:
    """
    python3 "${projectDir}/bin/rank_candidates.py" \\
      --screen ${screen_qc} \\
      --disease ${disease} \\
      --proteomics ${proteomics} \\
      --singlecell ${singlecell} \\
      --protein ${protein_features} \\
      --structure ${structure_features} \\
      --out candidate_rankings.tsv
    """
}

process LLM_EVIDENCE_CARDS {
    tag 'llm_evidence_cards'
    publishDir "${params.outdir}/evidence_cards", mode: 'copy'
    publishDir "${params.outdir}/app_data", mode: 'copy', pattern: 'evidence_cards.tsv'

    input:
    path rankings

    output:
    path 'evidence_cards.md'
    path 'evidence_cards.tsv'

    script:
    """
    python3 "${projectDir}/bin/make_evidence_cards.py" ${rankings} evidence_cards.md evidence_cards.tsv
    """
}

process REPORT {
    tag 'report'
    publishDir "${params.outdir}/reports", mode: 'copy', pattern: '*.html'
    publishDir "${params.outdir}/provenance", mode: 'copy', pattern: '*.json'

    input:
    path rankings
    path evidence_md

    output:
    path 'HTS_IL17_Psoriasis_report.html'
    path 'run_provenance.json'

    script:
    """
    python3 "${projectDir}/bin/make_report.py" ${rankings} ${evidence_md} HTS_IL17_Psoriasis_report.html run_provenance.json
    """
}

workflow {
    screen_file = file("${params.demo_data}/screen_assays.tsv")
    disease_file = file("${params.demo_data}/disease_omics.tsv")
    proteomics_file = file("${params.demo_data}/proteomics_validation.tsv")
    singlecell_file = file("${params.demo_data}/singlecell_context.tsv")
    protein_file = file("${params.demo_data}/protein_features.tsv")
    structure_file = file("${params.demo_data}/structure_features.tsv")

    fetched = FETCH_ASSAYS(screen_file)
    screen_qc = SCREEN_QC(fetched)
    disease = DISEASE_OMICS(disease_file)
    proteomics = PROTEOMICS_VALIDATE(proteomics_file)
    singlecell = SINGLECELL_CONTEXT(singlecell_file)
    protein_features = PROTEIN_EMBEDDINGS(protein_file)
    structure_features = STRUCTURE_FEATURES(structure_file)

    rankings = RANK_CANDIDATES(screen_qc, disease, proteomics, singlecell, protein_features, structure_features)
    cards = LLM_EVIDENCE_CARDS(rankings)
    REPORT(rankings, cards[0])
}
