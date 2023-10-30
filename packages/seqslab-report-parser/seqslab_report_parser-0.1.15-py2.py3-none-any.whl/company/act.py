import fitz

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util import pdf_util
from util.misc_util import *


def get_basic_info(test_name: str, pid: str, page: fitz.Page) -> Dict[str, List[str]]:
    search0 = page.search_for('Report No.:', hit_max=1)
    search1 = page.search_for('Date Reported:', hit_max=1)
    search2 = page.search_for('Diagnosis:', hit_max=1)
    search3 = page.search_for('Project ID:', hit_max=1)

    words = page.get_text('words')
    report_no = []
    date = []
    tumor = []
    patient_name = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir.y0 == search0[0].irect.y0 and ir.y1 == search0[0].irect.y1 and ir.x0 >= search0[0].irect.x1:
            report_no.append(w[4])
        if ir.y0 == search1[0].irect.y0 and ir.y1 == search1[0].irect.y1 and ir.x0 >= search1[0].irect.x1:
            date.append(w[4])
        if ir.y0 == search2[0].irect.y0 and ir.y1 == search2[0].irect.y1 and ir.x0 >= search2[0].irect.x1:
            tumor.append(w[4])
        if ir.y1 <= search3[0].irect.y0 and ir.x0 <= search3[0].irect.x0:
            patient_name.append(w[4])

    name = [patient_name[0]] if patient_name else []
    r = [report_no[0]] if report_no else []
    d = [' '.join(date)]
    idx = tumor.index('Lab') if 'Lab' in tumor else len(tumor)
    t = [' '.join(tumor[: idx])]

    return {
        REPORT_TEST_ASSAY: [test_name],
        REPORT_PATIENT_ID: [pid],
        REPORT_PATIENT_NAME: name,
        REPORT_ID: r,
        REPORT_DATE: d,
        REPORT_DIAGNOSIS: t
    }


def parse_v110(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str, output_dir: str) -> None:
    doc = fitz.Document(pdf_file_path)
    results = {
        'test_name': test_name,
        'label': patient_id,
    }

    (page, _, _) = pdf_util.find_table_location(
        doc,
        'ORDERING PHYSICIAN',
        'VARIANT(S) WITH CLINICAL RELEVANCE'
    )

    info = get_basic_info(test_name, patient_id, page)
    results['report'] = substitute_variables(template_report, info)

    page = doc.load_page(0)
    search1 = page.search_for('本次檢測於腫瘤檢體偵測到的重要基因變異及其相對應的標靶用藥如下', hit_max=1)
    search2 = page.search_for('腫瘤突變負荷量 (TMB)', hit_max=1)
    # Drug test result may not exist
    if search1 and search2:
        tab1 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0], header_rows=1)
        var1 = gen_variables(tab1, [BIOMARKER_MUTATION, SENSITIVE_DRUGS, RESISTANT_DRUGS])
        substitute_words(var1, {'\uf0b7': ''})
        r = []
        for v in var1:
            if v[SENSITIVE_DRUGS] != ['-']:
                v[BIOMARKER_EFFECT] = ['probable sensitive']
                v[BIOMARKER_ACTIONABLE_DRUG] = v[SENSITIVE_DRUGS]
                r.append(substitute_variables(template_biomarker_sens, v))
            if v[RESISTANT_DRUGS] != ['-']:
                v[BIOMARKER_EFFECT] = ['probable resistant']
                v[BIOMARKER_RESISTANT_DRUG] = v[RESISTANT_DRUGS]
                r.append(substitute_variables(template_biomarker_res, v))
        results['biomarker'] = r if r else None

    template2 = 'A variant involves in the {GENE} gene. The COSMIC ID for this mutation is {VARIANT_COSMIC}. ' \
                'The allele frequency indicates that approximately {VARIANT_ALLELE_FREQUENCY} of the sequenced reads ' \
                'carry this specific mutation. The coverage of {VARIANT_COVERAGE} suggests that this mutation has ' \
                'been observed in the given number of sequenced reads.'
    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'SINGLE NUCLEOTIDE AND SMALL INDEL VARIANTS',
        'COPY NUMBER VARIANTS (CNVS)'
    )
    tab2 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y0])
    var2 = gen_variables(tab2, [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_COVERAGE, VARIANT_ALLELE_FREQUENCY,
                                VARIANT_COSMIC])
    validate(patient_id, var2, [VARIANT_ALLELE_FREQUENCY])
    r = []
    for v in var2:
        r.append(substitute_variables(template2, v))
    results['significant_variant'] = r if r else None

    search1 = page.search_for('Amplification (Copy number ≥ 8) ', hit_max=1)
    search2 = page.search_for('Homozygous deletion (Copy number=0)', hit_max=1)
    search3 = page.search_for('Heterozygous deletion (Copy number=1)', hit_max=1)
    search4 = page.search_for('TUMOR MUTATIONAL BURDEN (TMB)', hit_max=1)
    search5 = page.search_for('行動基因僅提供技術檢測服務及檢測報告', hit_max=1)
    if search1[0].x0 == search2[0].x0:
        rect = [0, search1[0].y1, search3[0].x0 - 1, search2[0].y0]
    elif search4:
        rect = [0, search1[0].y1, search2[0].x0 - 1, search4[0].y0]
    else:
        rect = [0, search1[0].y1, search2[0].x0 - 1, search5[0].y0]
    tab3 = pdf_util.parse_table_by_cell(page, rect)
    var3 = gen_variables(tab3, [CHROMOSOME, GENE, COPY_NUMBER])
    validate(patient_id, var3, [CHROMOSOME])
    r = []
    for v in var3:
        v.update({VARIANT_FORM: ['Amplification']})
        r.append(substitute_variables(template_cna, v))

    if search2[0].x0 == search3[0].x0:
        rect = [search2[0].x0, search2[0].y1, 9999, search3[0].y0]
    elif search4:
        rect = [0, search2[0].y1, search3[0].x0, search4[0].y0]
    else:
        rect = [0, search2[0].y1, search3[0].x0, search5[0].y0]
    tab4 = pdf_util.parse_table_by_cell(page, rect)
    var4 = gen_variables(tab4, [CHROMOSOME, GENE])
    validate(patient_id, var4, [CHROMOSOME])
    for v in var4:
        v.update({VARIANT_FORM: ['Homozygous insertion'], COPY_NUMBER: ['0']})
        r.append(substitute_variables(template_cna, v))

    if search4:
        rect = [search3[0].x0, search3[0].y1, 9999, search4[0].y0]
    else:
        rect = [search3[0].x0, search3[0].y1, 9999, search5[0].y0]
    tab5 = pdf_util.parse_table_by_cell(page, rect)
    var5 = gen_variables(tab5, [CHROMOSOME, GENE])
    validate(patient_id, var5, [CHROMOSOME])
    for v in var5:
        v.update({VARIANT_FORM: ['Heterozygous deletion'], COPY_NUMBER: ['1']})
        r.append(substitute_variables(template_cna, v))
    results['cna'] = r if r else None

    r = [{
        "text": 'Immune checkpoint inhibitor biomarkers:',
        "tokens": ['Immune', 'checkpoint', 'inhibitor', 'biomarkers:'],
        "tags": ['O', 'O', 'O', 'O'],
        "tags_ids": [label_dict['O'], label_dict['O'], label_dict['O'], label_dict['O']]
    }]
    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'TUMOR MUTATIONAL BURDEN (TMB)',
        'Muts/Mb, mutations per megabase'
    )
    search3 = page.search_for('MICROSATELLITE INSTABILITY (MSI)', hit_max=1)
    tab6 = pdf_util.get_single_cell(page, [0, search1.y1, search3[0].x0, search2.y0])
    var6 = gen_variables(tab6, [TMB_RESULT])
    for v in var6:
        r.append(substitute_variables(template_ici_tmb, v))

    tab7 = pdf_util.get_single_cell(page, [search1.x1, search3[0].y1, 9999, search2.y0])
    var7 = gen_variables(tab7, [MSI_RESULT])
    for v in var7:
        r.append(substitute_variables(template_ici_msi, v))

    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'Genomic markers and alterations that are associated with response to ICI therapies',
        'MMR, mismatch repair; ND, not detected'
    )
    tab8 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y0])
    var8 = gen_variables(tab8, [POS_BIOMARKER, NEG_BIOMARKER])
    substitute_words(var8, {'ND': 'Not Detected', 'Yes': 'Yes'})
    for v in var8:
        if v[POS_BIOMARKER]:
            r.append(substitute_variables(template_ici_pos, v))
        if v[NEG_BIOMARKER]:
            r.append(substitute_variables(template_ici_neg, v))
    results['ici_biomarker'] = r if len(r) > 1 else None

    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'SINGLE NUCLEOTIDE AND SMALL INDEL VARIANTS',
        'Mutations with clinical relevance are highlighted in red.'
    )
    tab9 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y0])
    var9 = gen_variables(tab9, [GENE, CHROMOSOME, VARIANT_EXON, VARIANT_ACCESSION, VARIANT_HGVS,
                                VARIANT_AMINO_ACID_CHANGE, VARIANT_COVERAGE, VARIANT_ALLELE_FREQUENCY,
                                VARIANT_COSMIC])
    validate(patient_id, var9, [CHROMOSOME, VARIANT_ACCESSION, VARIANT_ALLELE_FREQUENCY])
    r = []
    for v in var9:
        r.append(substitute_variables(template_variant, v))
    results['variant'] = r if r else None

    if maf:
        results['maf'] = maf.to_maf(info[REPORT_PATIENT_ID][0], var9)

    if vcf:
        vcf.to_vcf('ACT', info[REPORT_PATIENT_ID][0], var9, output_dir)

    template_biomarker = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                         "\"{BIOMARKER_EFFECT}\" effects of clinical significance in relation to certain drugs " \
                         "{BIOMARKER_ACTIONABLE_DRUG} for the patient's tumor type."
    (page, search1, search2) = pdf_util.find_table_location(doc, 'TARGETED THERAPIES', 'Note')
    if page != -1 and not page.search_for('No genomic alterations predicted', hit_max=1):
        tab10 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 999, search2.y0])
        var10 = gen_variables(tab10, [BIOMARKER_MUTATION, BIOMARKER_EFFECT, BIOMARKER_ACTIONABLE_DRUG])
        r = []
        for v in var10:
            if v[BIOMARKER_MUTATION] and not v[BIOMARKER_MUTATION][0] == 'Level':
                r.append(substitute_variables(template_biomarker, v))
        results['biomarker'] = r if r else None

    write_json(results, output_dir, patient_id)


def parse_v111(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str, output_dir: str) -> None:
    doc = fitz.Document(pdf_file_path)
    results = {
        'test_name': test_name,
        'label': patient_id,
    }

    page = doc.load_page(0)
    info = get_basic_info(test_name, patient_id, page)
    results['report'] = substitute_variables(template_report, info)

    search1 = page.search_for('VARIANTS/BIOMARKERS WITH EVIDENCE OF CLINICAL SIGNIFICANCE', hit_max=1)
    search2 = page.search_for('VARIANTS/BIOMARKERS WITH POTENTIAL CLINICAL SIGNIFICANCE', hit_max=1)
    tab1 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0], header_rows=2)
    var1 = gen_variables(tab1, [BIOMARKER_MUTATION, SENSITIVE_DRUGS, RESISTANT_DRUGS, OTHER_SENSITIVE_DRUGS])
    r = []
    for v in var1:
        if v[SENSITIVE_DRUGS] != ['-']:
            v[BIOMARKER_EFFECT] = ['probable sensitive']
            v[BIOMARKER_ACTIONABLE_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_sens, v))
        if v[RESISTANT_DRUGS] != ['-']:
            v[BIOMARKER_EFFECT] = ['probable resistant']
            v[BIOMARKER_RESISTANT_DRUG] = v[RESISTANT_DRUGS]
            r.append(substitute_variables(template_biomarker_res, v))
        if v[OTHER_SENSITIVE_DRUGS] != ['-']:
            v[BIOMARKER_EFFECT] = ['probable sensitive']
            v[BIOMARKER_CANDIDATE_DRUG] = v[OTHER_SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_other, v))

    search1 = page.search_for('VARIANTS/BIOMARKERS WITH POTENTIAL CLINICAL SIGNIFICANCE', hit_max=1)
    search2 = page.search_for('Note:', hit_max=1)
    tab2 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0])
    var2 = gen_variables(tab2, [BIOMARKER_MUTATION, SENSITIVE_DRUGS, RESISTANT_DRUGS])
    for v in var2:
        if v[SENSITIVE_DRUGS] != ['-']:
            v[BIOMARKER_EFFECT] = ['possibly sensitive']
            v[BIOMARKER_ACTIONABLE_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_sens, v))
        if v[RESISTANT_DRUGS] != ['-']:
            v[BIOMARKER_EFFECT] = ['possibly resistant']
            v[BIOMARKER_RESISTANT_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_res, v))
    results['biomarker'] = r if r else None

    page = doc.load_page(1)
    search1 = page.search_for('- Copy Number Alterations', hit_max=1)
    search2 = page.search_for('- Fusions', hit_max=1)
    tab3 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0])
    var3 = gen_variables(tab3, [CHROMOSOME, GENE, VARIANT_FORM, COPY_NUMBER])
    validate(patient_id, var3, [CHROMOSOME])
    r = []
    for v in var3:
        r.append(substitute_variables(template_cna, v))
    results['cna'] = r if r else None

    search1 = page.search_for('- Fusions', hit_max=1)
    search2 = page.search_for('- Immune Checkpoint Inhibitor (ICI) Related Biomarkers', hit_max=1)
    tab4 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0])
    var4 = gen_variables(tab4, [FUSION_VARIANT, FUSION_TRANSCRIPT])
    r = []
    for v in var4:
        post_process(v)
        if VARIANT_FORM in v:
            r.append(substitute_variables(template_fusion, v))
        else:
            r.append(substitute_variables(template_fusion_no_variant_form, v))
    results['fusion'] = r if r else None

    r = [{
       "text": 'Immune checkpoint inhibitor biomarkers:',
       "tokens": ['Immune', 'checkpoint', 'inhibitor', 'biomarkers:'],
       "tags": ['O', 'O', 'O', 'O'],
       "tags_ids": [label_dict['O'], label_dict['O'], label_dict['O'], label_dict['O']]
    }]
    search1 = page.search_for('- Immune Checkpoint Inhibitor (ICI) Related Biomarkers', hit_max=1)
    search2 = page.search_for('Note:', hit_max=1)
    tab5 = pdf_util.parse_table_by_cell(page, [0, search1[0].y1, 9999, search2[0].y0])
    var5 = gen_variables(tab5, [BIOMARKER, RESULTS])
    for v in var5:
        if ' '.join(v[BIOMARKER]) == "Tumor Mutational Burden (TMB)":
            v[TMB_RESULT] = v[RESULTS]
            r.append(substitute_variables(template_ici_tmb, v))
        else:
            v[MSI_RESULT] = v[RESULTS]
            r.append(substitute_variables(template_ici_msi, v))
    results['ici_biomarker'] = r if len(r) > 1 else None

    (page, search1, search2) = pdf_util.find_table_location(doc, '- Single Nucleotide and Small InDel Variants',
                                                            '- Copy Number Alterations', 2)
    tab6 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y0])
    var6 = gen_variables(tab6, [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_EXON, VARIANT_HGVS,
                                VARIANT_ACCESSION, VARIANT_COSMIC, VARIANT_ALLELE_FREQUENCY, VARIANT_COVERAGE])
    validate(patient_id, var6, [VARIANT_ACCESSION, VARIANT_ALLELE_FREQUENCY])
    var7 = []
    r = []
    for v in var6:
        r.append(substitute_variables(template_variant, v))

    (page, search1, search2) = pdf_util.find_table_location(doc, 'OTHER DETECTED VARIANTS', 'Note:')
    if page != -1:
        tab7 = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y0])
        var7 = gen_variables(tab7, [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_EXON, VARIANT_HGVS,
                                    VARIANT_ACCESSION, VARIANT_COSMIC, VARIANT_ALLELE_FREQUENCY, VARIANT_COVERAGE])
        validate(patient_id, var7, [VARIANT_ACCESSION, VARIANT_ALLELE_FREQUENCY])
        for v in var7:
            r.append(substitute_variables(template_variant, v))
    results['variant'] = r if r else None

    if maf:
        results['maf'] = maf.to_maf(info[REPORT_PATIENT_ID][0], var6 + var7)

    if vcf:
        vcf.to_vcf('ACT', info[REPORT_PATIENT_ID][0], var6 + var7, output_dir)

    write_json(results, output_dir, patient_id)


def post_process(vars: Dict[str, List[str]]) -> None:
    pattern = r'(\w+)\((\d+)\)-(\w+)\((\d+)\)( \(.* variant (\w+)\))? fusion'
    pattern2 = r'.*\((.+)\), .*\((.+)\)'
    gene = ' '.join(vars[FUSION_VARIANT])
    (gene_a, exon_a, gene_b, exon_b, _, variant) = re.findall(pattern, gene)[0]
    if variant != '':
        vars[VARIANT_FORM] = [variant]

    transcript_id = ' '.join(vars[FUSION_TRANSCRIPT])
    (acc_num_a, acc_num_b) = re.findall(pattern2, transcript_id)[0]
    vars[FUSION_BREAKPOINT] = [f"exon {exon_a} of the {gene_a} gene and exon {exon_b} of the {gene_b} gene"]
    vars[FUSION_TRANSCRIPT] = [f"{acc_num_a} and {acc_num_b}"]
    vars[FUSION_GENE] = [f"{gene_a} and {gene_b}"]


def parse_act(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str,
        text_file_path: str,
        output_dir: str) -> None:
    doc = fitz.Document(pdf_file_path)
    page = doc.load_page(0)
    search1 = page.search_for('您好:', hit_max=1)
    search2 = page.search_for('REPORT SUMMARY', hit_max=1)
    pid = pdf_file_path[pdf_file_path.rfind('/') + 1: pdf_file_path.rfind('.')]\
        .replace('(', '')\
        .replace(')', '') if not patient_id else patient_id

    if search1 or search2:
        parse_v110(test_name, pid, maf, vcf, pdf_file_path, output_dir)
    else:
        parse_v111(test_name, pid, maf, vcf, pdf_file_path, output_dir)
