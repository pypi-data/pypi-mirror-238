import xml.etree.ElementTree as ET

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util.misc_util import *


def get_basic_info(test_name: str, pid: str, pdf_path: str, xml_path: str) -> Dict[str, List[str]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
        r = root.find('rr:CustomerInformation/rr:TRF', namespace).text
        first_name = root.find('rr:ResultsPayload/FinalReport/PMI/FirstName', namespace).text
        last_name = root.find('rr:ResultsPayload/FinalReport/PMI/LastName', namespace).text
        date = root.find('rr:ResultsPayload/FinalReport/PMI/CollDate', namespace).text
        tumor = root.find('rr:ResultsPayload/FinalReport/PMI/SubmittedDiagnosis', namespace).text

        return {
            REPORT_TEST_ASSAY: [test_name],
            REPORT_PATIENT_ID: [pid],
            REPORT_PATIENT_NAME: [f'{first_name} {last_name}'],
            REPORT_ID: [r],
            REPORT_DATE: [date],
            REPORT_DIAGNOSIS: [tumor]
        }
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_test_type(file_path: str) -> str:
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
    test_type = root.find('rr:ResultsPayload/FinalReport/Sample/TestType', namespace).text
    return test_type


def get_gene_findings_and_biomarkers(xml_path: str) -> (List[Dict[str, List[str]]], List[Dict[str, List[str]]]):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
        genes = root.findall('rr:ResultsPayload/FinalReport/Genes/Gene', namespace)
        biomarkers = []
        findings = []
        for gene in genes:
            b = {BIOMARKER: [], RESULTS: []}
            d = {BIOMARKER: [], SENSITIVE_DRUGS: [], OTHER_SENSITIVE_DRUGS: []}
            for child in gene:
                if child.tag == 'Name':
                    if len(child.text.split(' ')) > 1:
                        b[BIOMARKER] = [child.text]
                    else:
                        d[BIOMARKER].append(child.text)
                if child.tag == 'Alterations':
                    for alteration in child:
                        for a in alteration:
                            if a.tag == 'Name':
                                if b[BIOMARKER]:
                                    b[RESULTS] = [a.text]
                                else:
                                    d[BIOMARKER].append(a.text)
                            if a.tag == 'Therapies':
                                for therapy in a:
                                    fda_approved = False
                                    drug = ''
                                    for t in therapy:
                                        if t.tag == 'GenericName':
                                            drug = t.text
                                        if t.tag == 'FDAApproved' and t.text == 'true':
                                            fda_approved = True
                                    if fda_approved:
                                        d[SENSITIVE_DRUGS].append(drug)
                                    else:
                                        d[OTHER_SENSITIVE_DRUGS].append(drug)
            d[SENSITIVE_DRUGS] = list(set(d[SENSITIVE_DRUGS]))
            d[OTHER_SENSITIVE_DRUGS] = list(set(d[OTHER_SENSITIVE_DRUGS]))
            if d[BIOMARKER]:
                findings.append(d)
            if b[BIOMARKER]:
                biomarkers.append(b)

        return findings, biomarkers
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_variant(xml_path: str) -> List[Dict[str, List[str]]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting',
                     'vv': 'http://foundationmedicine.com/compbio/variant-report-external'}
        short_variants = root.findall('rr:ResultsPayload/vv:variant-report/vv:short-variants/vv:short-variant', namespace)
        variants = []
        for variant in short_variants:
            v = {
                GENE: [variant.attrib['gene']],
                VARIANT_POSITION: [variant.attrib['position']],
                VARIANT_HGVS: [variant.attrib['cds-effect']],
                VARIANT_AMINO_ACID_CHANGE: [variant.attrib['protein-effect']],
                VARIANT_COVERAGE: [variant.attrib['depth']],
                VARIANT_ALLELE_FRACTION: [variant.attrib['allele-fraction']],
                VARIANT_ACCESSION: [variant.attrib['transcript']],
                VARIANT_EFFECT: [variant.attrib['functional-effect']],
                VARIANT_STRAND: [variant.attrib['strand']]
            }

            variants.append(v)

        return variants
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_cnv(xml_path: str) -> List[Dict[str, List[str]]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting',
                     'vv': 'http://foundationmedicine.com/compbio/variant-report-external'}
        alterations = root.findall('rr:ResultsPayload/vv:variant-report/vv:copy-number-alterations/vv:copy-number-alteration', namespace)
        cnvs = []
        for a in alterations:
            v = {
                GENE: [a.attrib['gene']],
                CHROMOSOME: [a.attrib['position']],
                COPY_NUMBER: [a.attrib['copy-number']],
                VARIANT_FORM: [a.attrib['type']]
            }

            cnvs.append(v)

        return cnvs
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def parse_foundation_one(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str,
        xml_file_path: str,
        output_dir: str) -> None:
    pid = pdf_file_path[pdf_file_path.rfind('/') + 1: pdf_file_path.rfind('.')]\
        .replace('(', '')\
        .replace(')', '') if not patient_id else patient_id
    results = {
        'test_name': test_name,
        'label': pid,
    }
    basic_info = get_basic_info(test_name, pid, pdf_file_path, xml_file_path)
    results['report'] = substitute_variables(template_report, basic_info)

    r = [{
        "text": 'Immune checkpoint inhibitor biomarkers:',
        "tokens": ['Immune', 'checkpoint', 'inhibitor', 'biomarkers:'],
        "tags": ['O', 'O', 'O', 'O'],
        "tags_ids": [label_dict['O'], label_dict['O'], label_dict['O'], label_dict['O']]
    }]
    (findings, biomarkers) = get_gene_findings_and_biomarkers(xml_file_path)
    for b in biomarkers:
        if "Tumor Mutational Burden" in ' '.join(b[BIOMARKER]):
            b[TMB_RESULT] = b[RESULTS] + ["Muts/Mb"]
            r.append(substitute_variables(template_ici_tmb, b))
        elif "Microsatellite" in ''.join(b[BIOMARKER]):
            b[MSI_RESULT] = b[RESULTS]
            r.append(substitute_variables(template_ici_msi, b))
    results['ici_biomarker'] = r if len(r) > 1 else None

    r = []
    for v in findings:
        if v[SENSITIVE_DRUGS]:
            v[BIOMARKER_MUTATION] = v[BIOMARKER]
            v[BIOMARKER_EFFECT] = ['FDA-approved']
            v[BIOMARKER_ACTIONABLE_DRUG] = v[SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_sens, v))
        if v[OTHER_SENSITIVE_DRUGS]:
            v[BIOMARKER_MUTATION] = v[BIOMARKER]
            v[BIOMARKER_EFFECT] = ['FDA-approved']
            v[BIOMARKER_CANDIDATE_DRUG] = v[OTHER_SENSITIVE_DRUGS]
            r.append(substitute_variables(template_biomarker_other, v))
    results['biomarker'] = r if r else None

    # TODO
    template_foundation_variant = \
        "A DNA sequence variant {VARIANT_HGVS} is detected in the chromosome {VARIANT_POSITION} of the {GENE} gene " \
        "located on the {VARIANT_STRAND} strand, resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. The " \
        "variant allele frequency indicates that approximately {VARIANT_ALLELE_FRACTION} of the sequenced reads carry" \
        " this specific mutation with coverage of {VARIANT_COVERAGE}. This mutation causes {VARIANT_EFFECT} variant " \
        "effect. The transcripts associated with the variant are identified by the accession numbers " \
        "{VARIANT_ACCESSION}."
    r = []
    variants = get_variant(xml_file_path)
    for v in variants:
        r.append(substitute_variables(template_foundation_variant, v))
    results['variant'] = r if len(r) > 1 else None

    if maf:
        results['maf'] = maf.to_maf(basic_info[REPORT_PATIENT_ID][0], variants)

    if vcf:
        results['vcf'] = vcf.to_vcf('FOUNDATION', basic_info[REPORT_PATIENT_ID][0], variants, output_dir)

    # TODO
    template_foundation_cna = "In the chromosome {CHROMOSOME}, the genes {GENE} had undergone {VARIANT_FORM}," \
                              " resulting in a {COPY_NUMBER}-fold change in copy number."
    r = []
    cnvs = get_cnv(xml_file_path)
    for v in cnvs:
        r.append(substitute_variables(template_foundation_cna, v))
    results['cnv'] = r if len(r) > 1 else None

    write_json(results, output_dir, pid)
