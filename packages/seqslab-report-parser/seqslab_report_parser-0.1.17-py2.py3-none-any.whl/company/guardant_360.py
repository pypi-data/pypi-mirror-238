import fitz

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util import pdf_util
from util.misc_util import *


def get_basic_info(test_name: str, pid: str, page: fitz.Page, txt_path: str) -> Dict[str, List[str]]:
    search1 = page.search_for('Report Date:', hit_max=1)
    # 'Report Date:' not exists for reports that are amended or corrected
    if not search1:
        search1 = page.search_for('Original Reported Date:', hit_max=1)
    search2 = page.search_for('Diagnosis:', hit_max=1)

    words = page.get_text('words')
    date = []
    tumor = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir.y0 == search1[0].irect.y0 and ir.y1 == search1[0].irect.y1 and ir.x0 >= search1[0].irect.x1:
            date.append(w[4])
        if ir.y0 == search2[0].irect.y0 and ir.y1 == search2[0].irect.y1 and ir.x0 >= search2[0].irect.x1:
            tumor.append(w[4])

    d = [' '.join(date)]
    idx = tumor.index('|') if '|' in tumor else len(tumor)
    t = [' '.join(tumor[: idx])]

    return {
        REPORT_TEST_ASSAY: [test_name],
        REPORT_PATIENT_ID: [pid],
        REPORT_ID: [pid],
        REPORT_DATE: d,
        REPORT_DIAGNOSIS: t
    }


def get_patient_id(txt_path: str) -> str:
    try:
        with open(txt_path, 'r') as file:
            for line in file:
                if 'MP No.' in line:
                    pid = line.split(':')[1].replace('\n', '')
                    return pid
    except FileNotFoundError:
        print(f"File '{txt_path}' not found.")


def get_gene_alterations(page: fitz.Page) -> List[Dict[str, List[str]]]:
    search1 = page.search_for(
        'Summary of Detected Somatic Alterations, Immunotherapy Biomarkers & Associated Treatment Options', hit_max=1)
    search2 = page.search_for('Additional Biomarkers', hit_max=1)
    h1 = page.search_for('Detected Alteration(s) /', hit_max=1)
    h2 = page.search_for('Associated FDA-approved', hit_max=1)
    h3 = page.search_for('Clinical trial availability', hit_max=1)
    h4 = page.search_for('Amplification', hit_max=1)
    if not h1 and not h2 and not h3 and not h4:
        return []
    headers = [h1[0].irect, h2[0].irect, h3[0].irect, h4[0].irect]
    # header_rows=3 because 'KEY Approved in indication Approved in other indication Lack of response'
    # is considered as part of table
    tab = pdf_util.parse_table_by_header(page, [0, search1[0].y1, 9999, search2[0].y0], headers=headers, header_rows=2)
    updated_tab = post_process(tab)
    return gen_variables(updated_tab,
                         [BIOMARKER_MUTATION, SENSITIVE_DRUGS, OTHER_SENSITIVE_DRUGS, LACK_OF_RESPONSE, CF_DNA_OR_AMP])


# the original row of this table is:
# Before:
# Alteration/Biomarker, Therapies, Clinical trial, cfDNA % or Amplification
# After:
# Alteration/Biomarker, Therapies, Therapies in other indication, Lack of response, cfDNA % or Amplification
def post_process(table: List[List[List[str]]]) -> List[List[List[str]]]:
    tab_size = len(table)
    for i in range(0, tab_size):
        # put dfDNA of Amplification to last
        table[i].append([])
        table[i][-1] = table[i][3]
        # replace clinical trial with approved in other indication (OTHER_SENSITIVE_DRUGS)
        table[i][2] = ['None']
        # Lack of response
        table[i][3] = ['None']
        # Approved in other indication (OTHER_SENSITIVE_DRUGS)
        if i + 1 < tab_size and not table[i + 1][0]:
            table[i][2] = table[i + 1][1]
        # Lack of response
        if i + 2 < tab_size and not table[i + 2][0]:
            table[i][3] = table[i + 2][1]

    return list(filter(lambda i: i[0], table))


def get_biomarkers(txt_path: str) -> List[Dict[str, List[str]]]:
    try:
        with open(txt_path, 'r') as file:
            results = []
            in_biomarker = False
            b = {BIOMARKER: [], RESULTS: []}
            for line in file:
                if 'Biomarker:' in line:
                    b[BIOMARKER] = [line.split(':')[1].strip('\n []')]
                    in_biomarker = True
                elif in_biomarker:
                    b[RESULTS] = [line.split(':')[1].strip('\n []')]
                    results.append(b)
                    in_biomarker = False

            return results
    except FileNotFoundError:
        print(f"File '{txt_path}' not found.")


# def get_biomarkers(page: fitz.Page) -> List[Dict[str, List[str]]]:
#     search1 = page.search_for('Additional Biomarkers', hit_max=1)
#     # TODO:
#     search2 = page.search_for('', hit_max=1)
#     search3 = page.search_for('Biomarker')
#     search4 = page.search_for('Additional Details')
#     biomarker_hd = []
#     for s in search3:
#         if s.irect.y0 >= search1[0].irect.y0:
#             biomarker_hd.append(s.irect)
#     biomarker_hd.sort(key=lambda i: i.y0)
#
#     headers = [biomarker_hd[0], search4[0].irect]
#     tab = pdf_util.parse_table_by_header(page, [0, search1[0].y1, 9999, search2[0].y0], headers=headers, header_rows=2)
#     return gen_variables(tab, ['BIOMARKER', 'RESULTS'])


def parse_guardant_360(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str,
        text_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    doc = fitz.Document(pdf_file_path)
    page = doc.load_page(0)

    results = {
        'test_name': test_name,
        'label': patient_id,
    }
    basic_info = get_basic_info(test_name, patient_id, page, text_file_path)
    results['report'] = substitute_variables(template_report_no_name, basic_info)

    template_biomarker_no_therapy = "The genomic biomarker {BIOMARKER_MUTATION} is reported"
    var = get_gene_alterations(page)
    r = []
    for v in var:
        if v[SENSITIVE_DRUGS] != ['None']:
            v[BIOMARKER_EFFECT] = ['FDA-approved']
            v[BIOMARKER_ACTIONABLE_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_sens, v))
        if v[OTHER_SENSITIVE_DRUGS] != ['None']:
            v[BIOMARKER_EFFECT] = ['FDA-approved']
            v[BIOMARKER_CANDIDATE_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_other, v))
        if v[LACK_OF_RESPONSE] != ['None']:
            r.append(substitute_variables(template_biomarker_lack, v))
        if v[SENSITIVE_DRUGS] == ['None'] \
                and v[OTHER_SENSITIVE_DRUGS] == ['None'] \
                and v[LACK_OF_RESPONSE] == ['None']:
            r.append(substitute_variables(template_biomarker_no_therapy, v))
    results['biomarker'] = r if r else None

    r = []
    template_cfdna = "The variant allele fraction indicates that approximately {CF_DNA_OR_AMP} of cfDNA carry this " + \
                     "specific mutation."
    template_amp = "The patient sample indicates a {CF_DNA_OR_AMP} level of amplification carries this specific " + \
                   "mutation."
    for v in var:
        if '%' in v[CF_DNA_OR_AMP][0]:
            r.append(substitute_variables(template_cfdna, v))
        else:
            r.append(substitute_variables(template_amp, v))
    results['cfdna'] = r if r else None

    r = [{
        "text": 'Immune checkpoint inhibitor biomarkers:',
        "tokens": ['Immune', 'checkpoint', 'inhibitor', 'biomarkers:'],
        "tags": ['O', 'O', 'O', 'O'],
        "tags_ids": [label_dict['O'], label_dict['O'], label_dict['O'], label_dict['O']]
    }]
    var2 = get_biomarkers(text_file_path)
    for v in var2:
        r.append(substitute_variables(template_ici, v))
    results['ici_biomarker'] = r if r else None

    if maf:
        m = [{'Hugo_Symbol': v[BIOMARKER_MUTATION][0], 'Protein_Change': ' '.join(v[BIOMARKER_MUTATION][1:])} for v in var]
        results['maf'] = m

    return results, None, []
