from __future__ import annotations

import fitz

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util import pdf_util
from util.misc_util import *


def parse_assay(file_path: str) -> str:
    doc = fitz.Document(file_path)
    page = doc.load_page(0)
    search0 = page.search_for('Type:', hit_max=1)

    words = page.get_text('words')
    assay = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir.y0 == search0[0].irect.y0 and ir.y1 == search0[0].irect.y1 and ir.x0 >= search0[0].irect.x1:
            assay.append(w[4])

    return assay[-1]


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


def get_basic_info(pid: str, doc: fitz.Document) -> Dict[str, List[str]]:
    page = doc.load_page(0)
    search1 = page.search_for('Type:', hit_max=1)
    search2 = page.search_for('Job:', hit_max=1)
    search3 = page.search_for('Report Date:', hit_max=1)

    words = page.get_text('words')
    assay = []
    report_no = []
    date = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir.y0 == search1[0].irect.y0 and ir.y1 == search1[0].irect.y1 and ir.x0 >= search1[0].irect.x1:
            assay.append(w[4])
        if ir.y0 == search2[0].irect.y0 and ir.y1 == search2[0].irect.y1 and ir.x0 >= search2[0].irect.x1:
            report_no.append(w[4])
        if ir.y0 == search3[0].irect.y0 and ir.y1 == search3[0].irect.y1 and ir.x0 >= search3[0].irect.x1:
            date.append(w[4])

    tumor = []
    (page, search3) = pdf_util.find_first(doc, 'Disease:')
    if page:
        words = page.get_text('words')
        for w in words:
            ir = fitz.Rect(w[:4]).irect  # word rectangle
            if ir.y0 == search3[0].irect.y0 and ir.y1 == search3[0].irect.y1 and ir.x0 >= search3[0].irect.x1:
                tumor.append(w[4])

    a = [' '.join(assay)] if assay else []
    r = report_no if len(report_no) > 0 else []
    d = [date[0]] if date else []
    t = tumor if len(tumor) > 0 else []

    return {
        REPORT_TEST_ASSAY: a,
        REPORT_PATIENT_ID: [pid],
        REPORT_ID: r,
        REPORT_DATE: d,
        REPORT_DIAGNOSIS: t
    }


def parse_basic_info(pid: str, results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]], doc: fitz.Document) -> None:
    template_report = "The report {REPORT_TEST_ASSAY} for the patient  {REPORT_PATIENT_ID}) is issued on {REPORT_DATE}."
    template_diagnosis = "The diagnosis is {REPORT_DIAGNOSIS}."
    info = get_basic_info(pid, doc)
    if len(' '.join(info[REPORT_DIAGNOSIS])) == 0:
        results['report'] = substitute_variables(template_report, info)
    else:
        results['report'] = substitute_variables(template_report + ' ' + template_diagnosis, info)


def get_fusion(page: fitz.Page, search1: fitz.IRect, search2: fitz.IRect) -> Dict[str, List[str]]:
    tab = pdf_util.parse_table_by_cell(page, [0, search1.y1, 9999, search2.y1 + 10], header_rows=0)
    gene_a = tab[1][2][1].split('(')[0]
    gene_b = tab[1][2][5].split('(')[0]
    exon_a = tab[1][2][3].split(':')[1]
    exon_b = tab[1][2][7].split(':')[1]
    nm_a = tab[1][2][2].split(',')[0]
    nm_b = tab[1][2][6].split(',')[0]
    fusion_breakpoint = f"exon {exon_a} of the {gene_a} gene and exon {exon_a} of the {gene_b} gene"
    fusion_transcript = f"{nm_a} and {nm_b}"
    fusion_gene = f"{gene_a} and {gene_b}"
    fusion_variant = f"{gene_a}({exon_a})-{gene_b}({exon_b})"
    fusion = {
        'READS': [' '.join(tab[0][1][1:])],
        'GSP2': [' '.join(tab[1][0][1:-6])],  # use reverse index due to the number of column is not fixed
        'Mutation_Classification': [tab[1][0][-4]],
        'Is_Artifact': [tab[1][0][-1]],
        'Start_Sites': [tab[1][1][2]],
        FUSION_BREAKPOINT: [fusion_breakpoint],
        FUSION_GENE: [fusion_gene],
        FUSION_TRANSCRIPT: [fusion_transcript],
        FUSION_VARIANT: [fusion_variant],
        'Locus_a': [tab[1][2][0]],
        'Locus_b': [tab[1][2][4]]
    }

    return fusion


def parse_fusion(results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]], doc: fitz.Document,) -> None:
    (page, _) = pdf_util.find_first(doc, 'Reportable Isoforms')
    if page:
        tables = pdf_util.find_table_location_list(doc, 'Fusion:', 'Is Artifact', page.number)

        r = []
        for page, upper, lower in tables:
            var = get_fusion(page, upper, lower)
            r.append(substitute_variables(template_fusion_no_variant_form, var))

        results['fusion'] = r if r else None


def get_variant(pid: str, page: fitz.Page, search1: fitz.IRect, search2: fitz.IRect) -> Dict[str, List[str]]:
    cell = pdf_util.get_single_cell(page, [0, search1.y0 - 25, 9999, search1.y0])
    header = ''.join(cell[0][0]).split(':')
    hgvsp = header[1]
    tab = pdf_util.parse_table_by_cell(page, [0, search1.y0 - 10, 9999, search2.y1 + 10], header_rows=0)
    variant = {
        GENE: [tab[0][0][1]],
        VARIANT_REF: [tab[0][0][4]],
        VARIANT_MUTATION: [tab[0][0][6]],
        VARIANT_ALLELE_FRACTION: [tab[0][0][11]],
        'Mutation_Classification': [tab[0][0][14]],
        'Is_Artifact': [tab[0][0][17]],
        VARIANT_POSITION: [tab[0][1][1]],
        VARIANT_COVERAGE: [tab[0][1][3]],
        VARIANT_ACCESSION: [tab[0][1][-5]],  # use reverse index due to the number of column is not fixed
        VARIANT_AMINO_ACID_CHANGE: [hgvsp],
        'Sift': [tab[0][1][-3]],
        'PolyPhen': [tab[0][1][-1]]
    }
    validate(pid, [variant], [VARIANT_ALLELE_FRACTION, VARIANT_POSITION])

    return variant


def parse_variant(
        pid: str,
        results: Dict[str, str | Dict[str, str] | List[Dict[str, str]]],
        doc: fitz.Document,
        maf: MAF,
        vcf: VCF) -> (str, List[Dict[str, str]]):
    # TODO:
    template_variant = "A DNA sequence variant {VARIANT_REF}/{VARIANT_MUTATION} is detected in the {VARIANT_POSITION} " \
                       "of the {GENE} gene, resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. " \
                       "The variant allele frequency indicates that approximately {VARIANT_ALLELE_FRACTION} of " \
                       "the sequenced reads carry this specific mutation. The coverage of {VARIANT_COVERAGE} suggests " \
                       "that this mutation has been observed in the given number of sequenced reads. " \
                       "The protein associated with the variant are identified by " \
                       "the accession numbers {VARIANT_ACCESSION}."
    (page, _) = pdf_util.find_first(doc, 'Reportable Variants')
    if page:
        tables = pdf_util.find_table_location_list(doc, 'Gene:', 'PolyPhen', page.number)

        variant_descriptions = []
        all_variants = []
        for page, upper, lower in tables:
            var = get_variant(pid, page, upper, lower)
            all_variants.append(var)
            variant_descriptions.append(substitute_variables(template_variant, var))

        if len(all_variants) > 0:
            print(f'Archer: {pid}')
            results['variant'] = variant_descriptions
            if maf:
                results['maf'] = maf.archer_to_maf(pid, all_variants)
            if vcf:
                vcf_header, vcf = vcf.archer_to_vcf('Archer', pid, all_variants)
                return vcf_header, vcf
            else:
                return None, []

    return None, []


def parse_archer(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    (doc, results) = init(test_name, pdf_file_path, patient_id)
    parse_basic_info(patient_id, results, doc)
    vcf_header, vcf = parse_variant(patient_id, results, doc, maf, vcf)
    parse_fusion(results, doc)

    return results, vcf_header, vcf
