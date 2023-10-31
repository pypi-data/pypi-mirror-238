template_report = "The report {REPORT_TEST_ASSAY} (ID: {REPORT_ID}) for the patient {REPORT_PATIENT_NAME} (patient ID" \
                " {REPORT_PATIENT_ID}) is issued on {REPORT_DATE}. The diagnosis is {REPORT_DIAGNOSIS}."

template_report_no_name = "The report {REPORT_TEST_ASSAY} (ID: {REPORT_ID}) for the patient ID {REPORT_PATIENT_ID} " \
                          "is issued on {REPORT_DATE}. The diagnosis is {REPORT_DIAGNOSIS}."

template_biomarker_sens = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                          "\"{BIOMARKER_EFFECT}\" effects of clinical significance in relation to certain drugs " \
                          "{BIOMARKER_ACTIONABLE_DRUG} for the patient's tumor type."

template_biomarker_res = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                         "\"{BIOMARKER_EFFECT}\" effects of clinical significance in relation to certain drugs " \
                         "{BIOMARKER_RESISTANT_DRUG} for the patient's tumor type."

template_biomarker_other = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                           "\"{BIOMARKER_EFFECT}\" effects of clinical significance in relation to certain drugs " \
                           "{BIOMARKER_CANDIDATE_DRUG} for other tumor types."

template_biomarker_lack = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have lack of response " \
                          "of clinical significance in relation to certain drugs {LACK_OF_RESPONSE} for the " \
                          "patient's tumor type."

template_ici = 'Biomarker {BIOMARKER}: {RESULTS}.'

template_ici_tmb = 'Biomarker Tumor Mutational Burden (TMB): {TMB_RESULT}.'

template_ici_msi = 'Biomarker Microsatellite Instability (MSI): {MSI_RESULT}.'

template_ici_pos = 'Biomarker {POS_BIOMARKER}.'

template_ici_neg = 'Biomarker {NEG_BIOMARKER}.'

template_cna = "In the chromosome {CHROMOSOME}, the genes {GENE} had undergone {VARIANT_FORM}, " \
               "resulting in a {COPY_NUMBER} fold change in copy number."

template_fusion = "The {FUSION_VARIANT} is formed by the fusion of two separate genes, {FUSION_GENE}. " \
                  "The variant form is {VARIANT_FORM}. The fusion breakpoint occurs between " \
                  "{FUSION_BREAKPOINT}. The mRNA transcripts associated with the fusion genes {FUSION_GENE} are " \
                  "identified by the accession numbers {FUSION_TRANSCRIPT}, respectively."

template_fusion_no_variant_form = "The {FUSION_VARIANT} is formed by the fusion of two separate genes, {FUSION_GENE}. " \
                                  "The fusion breakpoint occurs between {FUSION_BREAKPOINT}. The mRNA transcripts " \
                                  "associated with the fusion genes {FUSION_GENE} are identified by the accession numbers " \
                                  "{FUSION_TRANSCRIPT}, respectively."

template_variant = "A DNA sequence variant {VARIANT_HGVS} is detected in the exon {VARIANT_EXON} of the {GENE} gene, " \
                   "resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. The COSMIC ID for this mutation " \
                   "is {VARIANT_COSMIC}. The variant allele frequency indicates that approximately "\
                   "{VARIANT_ALLELE_FREQUENCY} of the sequenced reads carry this specific mutation. The coverage of " \
                   "{VARIANT_COVERAGE} suggests that this mutation has been observed in the given number of " \
                   "sequenced reads. The transcripts associated with the variant are identified by the accession " \
                   "numbers {VARIANT_ACCESSION}."
