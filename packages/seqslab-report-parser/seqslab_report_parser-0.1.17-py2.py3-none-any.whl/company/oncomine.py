from __future__ import annotations

from typing import Callable

import fitz

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util import pdf_util
from util.misc_util import *

# TODO:
template_onco_biomarker_sens = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                               "\"sensitive\" effects of clinical significance in relation to certain drugs " \
                               "{BIOMARKER_ACTIONABLE_DRUG} for the patient's tumor type."

# TODO:
template_onco_biomarker_res = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have the " \
                              "\"resistant\" effects of clinical significance in relation to certain drugs " \
                              "{BIOMARKER_RESISTANT_DRUG} for the patient's tumor type."

# TODO:
template_onco_biomarker_other = "The genomic biomarker {BIOMARKER_MUTATION} is reported and known to have certain " \
                                "drugs {BIOMARKER_CANDIDATE_DRUG} for other tumor types."

# TODO:
template_onco_variant = "A DNA sequence variant {VARIANT_HGVS} is detected in the chromosome {VARIANT_POSITION} of " \
                        "the {GENE} gene, resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. The variant " \
                        "allele frequency indicates that approximately {VARIANT_ALLELE_FREQUENCY} of the sequenced " \
                        "reads carry this specific mutation. This mutation causes {VARIANT_EFFECT} effect. " \
                        "The transcripts associated with the variant are identified by the accession numbers " \
                        "{VARIANT_ACCESSION}."

# TODO:
template_onco_variant_frac = "A DNA sequence variant {VARIANT_HGVS} is detected in the chromosome {VARIANT_POSITION} of " \
                             "the {GENE} gene, resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. The variant " \
                             "allele frequency indicates that approximately {VARIANT_ALLELE_FRACTION} of the sequenced " \
                             "reads carry this specific mutation. This mutation causes {VARIANT_EFFECT} effect. " \
                             "The transcripts associated with the variant are identified by the accession numbers " \
                             "{VARIANT_ACCESSION}."

# TODO:
template_onco_cosmic = "The COSMIC ID for this mutation is {VARIANT_COSMIC}."

# TODO:
template_onco_coverage = "The coverage of {VARIANT_COVERAGE} suggests that this mutation has been observed in " \
                         "the given number of sequenced reads."

# TODO:
template_onco_clinvar = "The ClinVar result for this mutation is {CLIN_VAR}."


def parse_assay(file_path: str) -> str:
    doc = fitz.Document(file_path)
    page = doc.load_page(0)
    search0 = page.search_for('Assay:', hit_max=1)
    if not search0:
        return ''

    words = page.get_text('words')
    assay = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir.y0 == search0[0].irect.y0 and ir.y1 == search0[0].irect.y1 and ir.x0 >= search0[0].irect.x1:
            assay.append(w[4])

    # 'Oncomine Focus Assay'
    # 'Oncomine Myeloid Assay'
    # 'Oncomine Tumor Mutation Load Assay'
    # 'Oncomine BRCA1/2 Assay'

    return ' '.join(assay)


def init(
        test_name: str,
        pdf_file_path: str,
        patient_id: str) -> (fitz.Document, Dict[str, str | Dict[str, str]] | List[Dict[str, str]]):
    doc = fitz.Document(pdf_file_path)
    results = {
        'test_name': test_name,
        'label': patient_id,
    }

    return doc, results


def get_basic_info(pid: str, page: fitz.Page) -> Dict[str, List[str]]:
    search0 = page.search_for('Patient Name:', hit_max=1)
    search1 = page.search_for('Signing in Date:', hit_max=1)
    search2 = page.search_for('MP No.', hit_max=1)
    search3 = page.search_for('Assay:', hit_max=1)
    search4 = page.search_for('Sample Cancer Type:', hit_max=1)

    words = page.get_text('words')
    patient_name = []
    date = []
    report_no = []
    assay = []
    tumor = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if abs(ir.y0 - search0[0].irect.y0) <= pdf_util.TOLERANCE \
                and abs(ir.y1 - search0[0].irect.y1) <= pdf_util.TOLERANCE \
                and ir.x0 >= search0[0].irect.x1:
            patient_name.append(w[4])
        if ir.y0 == search1[0].irect.y0 and ir.y1 == search1[0].irect.y1 and ir.x0 >= search1[0].irect.x1:
            date.append(w[4])
        if ir.y0 == search2[0].irect.y0 and ir.y1 == search2[0].irect.y1 and ir.x0 >= search2[0].irect.x1:
            report_no.append(w[4])
        if ir.y0 == search3[0].irect.y0 and ir.y1 == search3[0].irect.y1 and ir.x0 >= search3[0].irect.x1:
            assay.append(w[4])
        if ir.y0 == search4[0].irect.y0 and ir.y1 == search4[0].irect.y1 and ir.x0 >= search4[0].irect.x1:
            tumor.append(w[4])

    a = [' '.join(assay)] if assay else []
    r = [report_no[0]] if report_no else []
    name = [patient_name[0]] if patient_name else []
    d = [date[0]] if date else []
    t = [' '.join(tumor)]

    return {
        REPORT_TEST_ASSAY: a,
        REPORT_PATIENT_ID: [pid],
        REPORT_PATIENT_NAME: name,
        REPORT_ID: r,
        REPORT_DATE: d,
        REPORT_DIAGNOSIS: t
    }


def parse_basic_info(pid: str, results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]], doc: fitz.Document) -> None:
    page = doc.load_page(0)
    info = get_basic_info(pid, page)
    results['report'] = substitute_variables(template_report, info)


def get_relevant_biomarkers(page: fitz.Page, search1, search2) -> List[Dict[str, List[str]]]:
    def post_process(tab: List[List[List[str]]], has_tier: bool) -> List[List[List[str]]]:
        new_tab = []
        for row in tab:
            if has_tier:
                updated_tier = list(filter(lambda i: i != '\xa0', row[0]))
                drug_for_this_cancer = rm_superscript(row[2])
                drug_for_others = rm_superscript(row[3])
                updated_row = [updated_tier, row[1], drug_for_this_cancer, drug_for_others, row[4]]
            else:
                drug_for_this_cancer = rm_superscript(row[1])
                drug_for_others = rm_superscript(row[2])
                updated_row = [row[0], drug_for_this_cancer, drug_for_others, row[3]]
            new_tab.append(updated_row)

        return new_tab

    h1 = page.search_for('Tier', hit_max=1)
    h2 = page.search_for('Genomic Alteration', hit_max=1)
    h3 = page.search_for('(In this cancer type)', hit_max=1)
    h4 = page.search_for('(In other cancer type)', hit_max=1)
    trials = page.search_for('Clinical Trials', hit_max=1)
    h5 = next(filter(lambda i: i.y0 == h2[0].y0, trials))
    if not h1 and not h2 and not h3 and not h4 and not h5:
        return []
    headers = [h1[0].irect, h2[0].irect, h3[0].irect, h4[0].irect, h5.irect] if h1 \
        else [h2[0].irect, h3[0].irect, h4[0].irect, h5.irect]
    tab = pdf_util.parse_table_by_header(page, [0, search1.y1, 9999, search2.y0], headers=headers, header_rows=1)
    if h1:
        column_names = [TIER, BIOMARKER_MUTATION, BIOMARKER_ACTIONABLE_DRUG, BIOMARKER_CANDIDATE_DRUG, TRIALS]
        updated_tab = post_process(tab, True)
    else:
        column_names = [BIOMARKER_MUTATION, BIOMARKER_ACTIONABLE_DRUG, BIOMARKER_CANDIDATE_DRUG, TRIALS]
        updated_tab = post_process(tab, False)
    return gen_variables(updated_tab, column_names)


def get_significant_biomarkers(page: fitz.Page, search1, search2) -> List[Dict[str, List[str]]]:
    def post_process(tab: List[List[List[str]]]) -> List[List[List[str]]]:
        new_tab = []
        for row in tab:
            k = None
            d = {'indicated': ['None'], 'contra': ['None']}
            for i in row[1]:
                if i == 'indicated' or i == 'contra':
                    k = i
                elif k:
                    d[k].append(i)

            indicated = rm_superscript(d['indicated'])
            contra = rm_superscript(d['contra'])
            others = rm_superscript(row[2])
            updated_row = [row[0], indicated, contra, others, row[3]]
            new_tab.append(updated_row)

        return new_tab

    h1 = page.search_for('Genomic Alteration', hit_max=1)
    h2 = page.search_for('(In this cancer type)', hit_max=1)
    h3 = page.search_for('(In other cancer type)', hit_max=1)
    trials = page.search_for('Clinical Trials', hit_max=1)
    h4 = next(filter(lambda i: i.y0 == h1[0].y0, trials))
    if not h1 and not h2 and not h3 and not h4:
        return []
    headers = [h1[0].irect, h2[0].irect, h3[0].irect, h4.irect]
    indicated = pdf_util.get_particular_drawing_rect(
        page,
        [0, h1[0].y1, 9999, search2.y0],
        lambda i: 'fill' in i and i['fill'] is not None and round(i['fill'][1]) == 1
    )
    contra_indicated = pdf_util.get_particular_drawing_rect(
        page,
        [0, h1[0].y1, 9999, search2.y0],
        lambda i: 'fill' in i and i['fill'] is not None and round(i['fill'][0]) == 1
    )
    # reason to subtract TOLERANCE:
    # in parse_table_by_header(), words will be sorted by y-axis then x-axis,
    # and we want drugs are preceded by `indicated` or `contra`
    indicated_word = list(map(lambda i: (i.x0, i.y0 - pdf_util.TOLERANCE, i.x1, i.y1, 'indicated'), indicated))
    contra_word = list(map(lambda i: (i.x0, i.y0 - pdf_util.TOLERANCE, i.x1, i.y1, 'contra'), contra_indicated))
    tab = pdf_util.parse_table_by_header(
        page,
        [0, search1.y1, 9999, search2.y0],
        headers=headers,
        header_rows=1,
        additional_words=indicated_word + contra_word
    )
    updated_tab = post_process(tab)
    return gen_variables(updated_tab,
                         [BIOMARKER_MUTATION, BIOMARKER_ACTIONABLE_DRUG, BIOMARKER_RESISTANT_DRUG, BIOMARKER_CANDIDATE_DRUG, TRIALS])


def parse_biomarkers(
        results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]],
        doc: fitz.Document,
        template_sens: str,
        template_res: str,
        template_other: str) -> None:
    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'Relevant Biomarkers',
        'Public data sources included in relevant therapies'
    )
    rel_var = []
    if page != -1:
        rel_var = get_relevant_biomarkers(page, search1, search2)

    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'Clinically Significant Biomarkers',
        'Sources included in relevant therapies'
    )
    sig_var = []
    if page != -1:
        sig_var = get_significant_biomarkers(page, search1, search2)

    r = []
    # TODO: should we separate significant & relevant ?
    for v in rel_var + sig_var:
        if v.get(BIOMARKER_ACTIONABLE_DRUG, ['None']) != ['None']:
            r.append(substitute_variables(template_sens, v))
        if v.get(BIOMARKER_RESISTANT_DRUG, ['None']) != ['None']:
            r.append(substitute_variables(template_res, v))
        if v.get(BIOMARKER_CANDIDATE_DRUG, ['None']) != ['None']:
            r.append(substitute_variables(template_other, v))
    results['biomarker'] = r if r else None


def get_clinvar_variants(pid: str, page: fitz.Page) -> List[Dict[str, List[str]]]:
    search1 = page.search_for('DNA Sequence Variants', hit_max=1)
    search2 = page.search_for('1 Based on Clinvar version', hit_max=1)
    search3 = page.search_for('Copy Number Variations', hit_max=1)
    search4 = page.search_for('Disclaimer', hit_max=1)
    if search2:
        bottom = search2[0]
    elif search3:
        bottom = search3[0]
    else:
        s = search4[0]
        bottom = fitz.Rect(s.x0, s.y0 - 10, s.x1, s.y1)
    if not search1:
        return []

    gene_txt = page.search_for('Gene')
    locus_txt = page.search_for('Locus', hit_max=1)
    freq_txt = page.search_for('Frequency')
    frac_txt = page.search_for('Fraction')
    variant_id_txt = page.search_for('Variant ID', hit_max=1)
    clinvar_txt = page.search_for('ClinVar', hit_max=1)

    aac = page.search_for('Amino Acid Change', hit_max=1)[0]
    gene = next(filter(lambda i: i.y0 == aac.y0, gene_txt))
    coding = page.search_for('Coding', hit_max=1)[0]
    variant_id = variant_id_txt[0] if variant_id_txt else None
    locus = next(filter(lambda i: i.y0 == aac.y0, locus_txt))
    freq = next(filter(lambda i: i.y0 == aac.y0, freq_txt + frac_txt))
    trans = page.search_for('Transcript', hit_max=1)[0]
    var_effect = page.search_for('Variant Effect', hit_max=1)[0]
    clinvar = clinvar_txt[0] if clinvar_txt else None
    cov = page.search_for('Coverage', hit_max=1)[0]
    if not gene and not aac and not coding and not variant_id and not locus and \
            not freq and not trans and not var_effect and not clinvar and not cov:
        return []

    if clinvar:
        if variant_id:
            header_pos = [gene.irect, aac.irect, coding.irect, variant_id.irect, locus.irect,
                          freq.irect, trans.irect, var_effect.irect, clinvar.irect, cov.irect]
            headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_COSMIC, VARIANT_POSITION,
                       VARIANT_ALLELE_FREQUENCY, VARIANT_ACCESSION, VARIANT_EFFECT, CLIN_VAR, VARIANT_COVERAGE]
        else:
            header_pos = [gene.irect, aac.irect, coding.irect, locus.irect,
                          freq.irect, trans.irect, var_effect.irect, clinvar.irect, cov.irect]
            headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_POSITION,
                       VARIANT_ALLELE_FREQUENCY, VARIANT_ACCESSION, VARIANT_EFFECT, CLIN_VAR, VARIANT_COVERAGE]
    else:
        if variant_id:
            header_pos = [gene.irect, aac.irect, coding.irect, variant_id.irect, locus.irect,
                          freq.irect, trans.irect, var_effect.irect, cov.irect]
            headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_COSMIC, VARIANT_POSITION,
                       VARIANT_ALLELE_FREQUENCY, VARIANT_ACCESSION, VARIANT_EFFECT, VARIANT_COVERAGE]
        else:
            header_pos = [gene.irect, aac.irect, coding.irect, locus.irect,
                          freq.irect, trans.irect, var_effect.irect, cov.irect]
            headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_POSITION,
                       VARIANT_ALLELE_FREQUENCY, VARIANT_ACCESSION, VARIANT_EFFECT, VARIANT_COVERAGE]
    # set header_rows to 0 because no borderline above headers
    tab = pdf_util.parse_table_by_header(page, [0, search1[0].y1, 9999, bottom.y0], headers=header_pos, header_rows=0)
    return gen_variables(tab, headers)


def get_variants(pid: str, page: fitz.Page) -> List[Dict[str, List[str]]]:
    search1 = page.search_for('DNA Sequence Variants', hit_max=1)
    search2 = page.search_for('1 Based on Clinvar version', hit_max=1)
    search3 = page.search_for('Copy Number Variations', hit_max=1)
    search4 = page.search_for('Relevant Therapy Summary', hit_max=1)
    search5 = page.search_for('Gene Fusions (RNA)', hit_max=1)
    search6 = page.search_for('Biomarker Descriptions', hit_max=1)
    search7 = page.search_for('Disclaimer:', hit_max=1)
    if not search1:
        return []

    gene = page.search_for('Gene')
    locus = page.search_for('Locus', hit_max=1)
    freq = page.search_for('Frequency')
    frac = page.search_for('Fraction')
    transcript = page.search_for('Transcript', hit_max=1)
    h2 = page.search_for('Amino Acid Change', hit_max=1)
    h3 = page.search_for('Coding', hit_max=1)
    h4 = page.search_for('Variant ID', hit_max=1)
    h7 = page.search_for('Transcript', hit_max=1)
    h8 = page.search_for('Variant Effect', hit_max=1)
    h9 = page.search_for('Coverage', hit_max=1)
    h1 = next(filter(lambda i: i.y0 == h2[0].y0, gene))
    h5 = next(filter(lambda i: i.y0 == h2[0].y0, locus))
    h6 = next(filter(lambda i: i.y0 == h2[0].y0, freq + frac))
    h7 = next(filter(lambda i: i.y0 == h2[0].y0, transcript))
    if not h1 and not h2 and not h3 and not h4 and not h5 and not h6 and not h7 and not h8 and not h9:
        return []

    bottom = None
    for idx, s in enumerate([search2, search3, search4, search5, search6]):
        if not bottom and s:
            bottom = s[0]
        elif bottom and s and search1[0].y1 < s[0].y0 < bottom.y0:
            bottom = s[0]
    if not bottom:
        # "Disclaimer:" always at the bottom of page
        s = search7[0]
        bottom = fitz.Rect(s.x0, s.y0 - 10, s.x1, s.y1)

    freq_len = len(list(filter(lambda i: i.y0 == h2[0].y0, freq)))
    af = VARIANT_ALLELE_FREQUENCY if freq_len > 0 else VARIANT_ALLELE_FRACTION
    if h9:
        header_pos = [h1.irect, h2[0].irect, h3[0].irect, h4[0].irect,
                      h5.irect, h6.irect, h7.irect, h8[0].irect, h9[0].irect]
        headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_COSMIC, VARIANT_POSITION,
                   af, VARIANT_ACCESSION, VARIANT_EFFECT, VARIANT_COVERAGE]
    else:
        header_pos = [h1.irect, h2[0].irect, h3[0].irect, h4[0].irect,
                      h5.irect, h6.irect, h7.irect, h8[0].irect]
        headers = [GENE, VARIANT_AMINO_ACID_CHANGE, VARIANT_HGVS, VARIANT_COSMIC, VARIANT_POSITION,
                   af, VARIANT_ACCESSION, VARIANT_EFFECT]
    # set header_rows to 0 because no borderline above headers
    tab = pdf_util.parse_table_by_header(page, [0, search1[0].y1, 9999, bottom.y0], headers=header_pos, header_rows=0)
    variants = gen_variables(tab, headers)
    validate(pid, variants, [VARIANT_POSITION, af, VARIANT_ACCESSION])

    return variants


def parse_variants(
        pid: str,
        results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]],
        doc: fitz.Document,
        func: Callable[[str, fitz.Page], List[Dict[str, List[str]]]],
        template_variant: str,
        template_variant_frac: str,
        template_cosmic: str,
        template_coverage: str,
        template_clinvar: str,
        maf: MAF,
        vcf: VCF) -> (str, List[Dict[str, str]]):
    (begin, end) = doc.last_location
    all_variants = []
    # variants table may cross many pages
    for i in range(begin, end + 1):
        page = doc.load_page(i)
        vars = func(pid, page)
        if vars:
            all_variants += vars
    template = ''
    if all_variants:
        keys = list(all_variants[0].keys())
        if VARIANT_COSMIC in keys:
            template = template_cosmic
        if VARIANT_COVERAGE in keys:
            template = template_coverage
        if CLIN_VAR in keys:
            template = template_clinvar
    r = []
    for v in all_variants:
        if VARIANT_ALLELE_FREQUENCY in v.keys():
            if template:
                t = template_variant + ' ' + template
            else:
                t = template_variant
        else:
            if template:
                t = template_variant_frac + ' ' + template
            else:
                t = template_variant_frac
        r.append(substitute_variables(t, v))
    results['variant'] = r if r else None

    if maf:
        results['maf'] = maf.to_maf(pid, all_variants)

    if vcf:
        vcf_header, vcf = vcf.to_vcf('ONCOMINE', pid, all_variants)
        return vcf_header, vcf
    else:
        return None, []


def get_cnv(pid: str, page: fitz.Page, search1, search2) -> List[Dict[str, List[str]]]:
    def check_cnv(locus: List[str]) -> bool:
        if locus:
            return ''.join(locus).startswith('chr')
        else:
            return False

    if not search1:
        return []

    h1 = next(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Gene', hit_max=1)))
    h2 = next(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Locus', hit_max=1)))
    h3 = page.search_for('Copy Number', hit_max=1)
    if not h1 and not h2 and not h3:
        return []

    headers = [h1.irect, h2.irect, h3[0].irect]
    # set header_rows to 0 because no borderline above headers
    tab = pdf_util.parse_table_by_header(page, [0, search1.y1, 9999, search2.y0], headers=headers, header_rows=0)
    vars = gen_variables(tab, [GENE, VARIANT_POSITION, COPY_NUMBER])
    cnv = list(filter(lambda i: check_cnv(i[VARIANT_POSITION]), vars))
    validate(pid, cnv, [VARIANT_POSITION])

    return cnv


def parse_cnv(pid: str, results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]], doc: fitz.Document) -> None:
    # TODO:
    template_cnv = "In the chromosome {VARIANT_POSITION}, the genes {GENE} had a {COPY_NUMBER}-fold change in copy number."

    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'Copy Number Variations',
        'Biomarker Descriptions'
    )

    if page == -1:
        (page, search1, search2) = pdf_util.find_table_location(
            doc,
            'Copy Number Variations',
            'Disclaimer:'
        )
        if page == -1:
            return

    var = get_cnv(pid, page, search1, search2)
    r = []
    for v in var:
        r.append(substitute_variables(template_cnv, v))
    results['cnv'] = r if r else None


def get_fusion(page: fitz.Page, search1, search2) -> List[Dict[str, List[str]]]:
    def check_locus(locus: List[str]) -> bool:
        if locus:
            return ''.join(locus).startswith('chr')
        else:
            return False

    def post_process(vars: Dict[str, List[str]]) -> None:
        pattern = r'(\w+)-(\w+)\.\w([0-9a-fA-F]+)\w([0-9a-fA-F]+).*'
        gene = ' '.join(vars[FUSION_VARIANT])
        (gene_a, gene_b, exon_a, exon_b) = re.findall(pattern, gene)[0]
        vars[FUSION_BREAKPOINT] = [f"exon {exon_b} of the {gene_b} gene and exon {exon_a} of the {gene_a} gene"]
        vars[FUSION_GENE] = [f"{gene_b} and {gene_a}"]

    if not search1:
        return []

    h1 = next(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Genes', hit_max=1)))
    h2 = next(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Variant ID', hit_max=1)))
    h3 = next(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Locus', hit_max=1)))
    h4 = list(filter(lambda i: search1.y1 < i.y1 < search2.y1, page.search_for('Read Count', hit_max=1)))
    if not h1 and not h2 and not h3 and not h4:
        return []

    if h4:
        headers = [h1.irect, h2.irect, h3.irect, h4[0].irect]
        header_titles = [FUSION_GENE, FUSION_VARIANT, FUSION_LOCUS, FUSION_READ_COUNT]
    else:
        headers = [h1.irect, h2.irect, h3.irect]
        header_titles = [FUSION_GENE, FUSION_VARIANT, FUSION_LOCUS]
    # set header_rows to 0 because no borderline above headers
    tab = pdf_util.parse_table_by_header(page, [0, search1.y1, 9999, search2.y0], headers=headers, header_rows=0)
    fusion = gen_variables(tab, header_titles)
    filtered = list(filter(lambda i: check_locus(i[FUSION_LOCUS]), fusion))
    for f in filtered:
        post_process(f)

    return filtered


def parse_fusion(results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]], doc: fitz.Document,) -> None:
    template_fusion = "The {FUSION_VARIANT} is formed by the fusion of two separate genes, {FUSION_GENE}. " \
                      "The fusion breakpoint occurs between {FUSION_BREAKPOINT}."

    (page, search1, search2) = pdf_util.find_table_location(
        doc,
        'Gene Fusions (RNA)',
        'Biomarker Descriptions'
    )

    if page == -1:
        (page, search1, search2) = pdf_util.find_table_location(
            doc,
            'Gene Fusions (RNA)',
            'Disclaimer:'
        )
        if page == -1:
            return

    var = get_fusion(page, search1, search2)
    r = []
    for v in var:
        r.append(substitute_variables(template_fusion, v))
    results['fusion'] = r if r else None


def parse_brca(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    (doc, results) = init(test_name, pdf_file_path, patient_id)
    parse_basic_info(patient_id, results, doc)
    parse_biomarkers(results, doc, template_onco_biomarker_sens, template_onco_biomarker_res, template_onco_biomarker_other)
    vcf_header, vcf = parse_variants(patient_id, results, doc, get_clinvar_variants,
                                     template_onco_variant, template_onco_variant_frac, template_onco_cosmic, template_onco_coverage, template_onco_clinvar,
                                     maf, vcf)
    parse_cnv(patient_id, results, doc)
    parse_fusion(results, doc)

    return results, vcf_header, vcf


def parse_focus(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    (doc, results) = init(test_name, pdf_file_path, patient_id)
    parse_basic_info(patient_id, results, doc)
    parse_biomarkers(results, doc, template_onco_biomarker_sens, template_onco_biomarker_res, template_onco_biomarker_other)
    vcf_header, vcf = parse_variants(patient_id, results, doc, get_variants,
                                     template_onco_variant, template_onco_variant_frac, template_onco_cosmic, template_onco_coverage, template_onco_clinvar,
                                     maf, vcf)
    parse_cnv(patient_id, results, doc)
    parse_fusion(results, doc)

    return results, vcf_header, vcf


def parse_myeloid(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    (doc, results) = init(test_name, pdf_file_path, patient_id)
    parse_basic_info(patient_id, results, doc)
    parse_biomarkers(results, doc, template_onco_biomarker_sens, template_onco_biomarker_res, template_onco_biomarker_other)
    vcf_header, vcf = parse_variants(patient_id, results, doc, get_variants,
                                     template_onco_variant, template_onco_variant_frac, template_onco_cosmic, template_onco_coverage, template_onco_clinvar,
                                     maf, vcf)
    parse_cnv(patient_id, results, doc)
    parse_fusion(results, doc)

    return results, vcf_header, vcf


def parse_tumor_mutation_load(test_name: str, patient_id: str, maf: MAF, vcf: VCF, pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    (doc, results) = init(test_name, pdf_file_path, patient_id)
    parse_basic_info(patient_id, results, doc)
    parse_biomarkers(results, doc, template_onco_biomarker_sens, template_onco_biomarker_res, template_onco_biomarker_other)
    vcf_header, vcf = parse_variants(patient_id, results, doc, get_variants,
                                     template_onco_variant, template_onco_variant_frac, template_onco_cosmic, template_onco_coverage, template_onco_clinvar,
                                     maf, vcf)
    parse_cnv(patient_id, results, doc)
    parse_fusion(results, doc)

    return results, vcf_header, vcf


def parse_oncomine(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    if 'BRCA' in test_name:
        return parse_brca(test_name, patient_id, maf, vcf, pdf_file_path)
    elif test_name == 'Oncomine Focus Assay':
        return parse_focus(test_name, patient_id, maf, vcf, pdf_file_path)
    elif test_name == 'Oncomine Myeloid Assay':
        return parse_myeloid(test_name, patient_id, maf, vcf, pdf_file_path)
    elif 'Tumor Mutation Load' in test_name:
        return parse_tumor_mutation_load(test_name, patient_id, maf, vcf, pdf_file_path)
    else:
        raise NotImplementedError(test_name)
