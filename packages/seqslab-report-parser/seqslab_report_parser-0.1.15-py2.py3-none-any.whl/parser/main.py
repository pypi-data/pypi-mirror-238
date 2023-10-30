from collections import deque
from typing import Dict
import argparse
import csv
import json
import os
import threading
import traceback
import sys
if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

import mysql.connector
from pyfaidx import Fasta
from pyhgvs.models import Transcript
from pyhgvs.utils import read_transcripts

from genomics.maf import MAF
from genomics.vcf import VCF
from util.parse_gencode import parse_transcript_cds
from company import act, archer, foundation_one, guardant_360, oncomine


def get_files(root, files) -> (str, str, str):
    pdf_file_path = None
    txt_file_path = None
    xml_file_path = None
    for f in files:
        if f.endswith('pdf'):
            pdf_file_path = os.path.join(root, f)
        elif f.endswith('txt'):
            txt_file_path = os.path.join(root, f)
        elif f.endswith('xml'):
            xml_file_path = os.path.join(root, f)

    return pdf_file_path, txt_file_path, xml_file_path


def bfs_traverse(input_dir: str, output_dir: str, maf: MAF, vcf: VCF):
    queue = deque([input_dir])
    threads = []

    while queue:
        vertex = queue.popleft()
        for root, dirs, files in os.walk(vertex):
            # handle reports do not have well organized folder structure
            if sum(1 for item in files if item.endswith(".pdf")) > 1:
                for f in files:
                    pdf_file_path = os.path.join(root, f)
                    t = threading.Thread(
                        target=parse_report('', maf, vcf, pdf_file_path, None, None, output_dir))
                    t.start()
                    threads.append(t)
            elif files:
                pdf_file_path, txt_file_path, xml_file_path = get_files(root, files)
                if pdf_file_path is None:
                    continue

                t = threading.Thread(
                    target=parse_report('', maf, vcf, pdf_file_path, txt_file_path, xml_file_path, output_dir))
                t.start()
                threads.append(t)
            else:
                for d in dirs:
                    queue.append(d)
    for t in threads:
        t.join()


def get_test_name(pdf_file_path: str, txt_file_path: str, xml_file_path: str) -> str:
    def parse_txt_test_name(file_path: str, encoding) -> str:
        with open(file_path, 'r', encoding=encoding) as file:
            for line in file:
                if 'Test Name:' in line:
                    test_name = line.split(':')[1].replace('\n', '').strip()
                    return test_name
                if 'ACTOnco' in line:
                    return 'ACTOnco+'
                if 'FoundationOne CDX' in line:
                    return 'FoundationOne CDX'
                if 'Guardant360' in line:
                    return 'Guardant360'

    try:
        if txt_file_path is None and xml_file_path is None:
            assay = oncomine.parse_assay(pdf_file_path)
            if assay:
                return assay
            else:
                return archer.parse_assay(pdf_file_path)
        elif txt_file_path:
            return parse_txt_test_name(txt_file_path, encoding=None)
        else:
            return foundation_one.get_test_type(xml_file_path)
    except UnicodeDecodeError:
        # for FoundationOne
        return parse_txt_test_name(txt_file_path, encoding='iso-8859-1')
    except FileNotFoundError:
        print(f"File '{txt_file_path}' not found.")


def parse_report(
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str,
        txt_file_path: str,
        xml_file_path: str,
        output_dir: str) -> None:
    try:
        print('begin parse ', pdf_file_path)

        test_name = get_test_name(pdf_file_path, txt_file_path, xml_file_path)
        if test_name == 'ACTOnco+':
            act.parse_act(test_name, patient_id, maf, vcf, pdf_file_path, txt_file_path, output_dir)
        elif test_name.startswith('FoundationOne'):
            foundation_one.parse_foundation_one(test_name, patient_id, maf, vcf, pdf_file_path, xml_file_path,
                                                output_dir)
        elif test_name == 'Guardant360':
            guardant_360.parse_guardant_360(test_name, patient_id, maf, vcf, pdf_file_path, txt_file_path,
                                            output_dir)
        elif test_name.startswith('Oncomine') or test_name.startswith('Tumor Mutation Load Assay'):
            oncomine.parse_oncomine(test_name, patient_id, maf, vcf, pdf_file_path, output_dir)
        elif test_name.startswith('Archer'):
            archer.parse_archer(test_name, patient_id, maf, vcf, pdf_file_path, output_dir)
        else:
            raise RuntimeError('Test {} not support'.format(test_name))

        print('end parse ', pdf_file_path)
    except Exception:
        print('end parse failed ', pdf_file_path)
        traceback.print_exc()


def batch(args):
    check_resource(args)
    gen_maf = args.maf
    gen_vcf = args.vcf
    genome, transcripts, cds, nm_to_ens = init_resource(args) if gen_maf or gen_vcf else (None, None, None, None)

    dst = args.output_dir
    os.makedirs(dst, exist_ok=True)
    maf = MAF(genome, transcripts, cds, nm_to_ens, args.ref, args.ref_gene) if gen_maf else None
    vcf = VCF(genome, transcripts, cds, nm_to_ens, args.ref, args.ref_fai, args.ref_gene) if gen_vcf else None
    bfs_traverse(args.input_dir, dst, maf, vcf)


def single(args):
    check_resource(args)
    gen_maf = args.maf
    gen_vcf = args.vcf
    genome, transcripts, cds, nm_to_ens = init_resource(args) if gen_maf or gen_vcf else (None, None, None, None)

    for root, dirs, files in os.walk(args.input_dir):
        pdf_file_path, txt_file_path, xml_file_path = get_files(root, files)
        out = args.output_dir
        pid = args.pid

        maf = MAF(genome, transcripts, cds, nm_to_ens, args.ref, args.ref_gene) if gen_maf else None
        vcf = VCF(genome, transcripts, cds, nm_to_ens, args.ref, args.ref_fai, args.ref_gene) if gen_vcf else None
        parse_report(pid, maf, vcf, pdf_file_path, txt_file_path, xml_file_path, out)


def check_resource(args):
    if args.maf or args.vcf:
        if not os.path.exists(args.ref):
            raise RuntimeError(f'Genome reference not exists: {args.ref}')
        if not os.path.exists(args.ref_fai):
            raise RuntimeError(f'Index of Genome reference not exists: {args.ref_fai}')
        if not os.path.exists(args.ref_gene):
            raise RuntimeError(f'genes.refGene not exists: {args.ref_gene}')
        if not os.path.exists(args.trans_cds):
            raise RuntimeError(f'transcript_cds.json not exists: {args.trans_cds}')


def init_resource(args) -> (Fasta, Dict[str, Transcript], Dict, Dict[str, str]):
    genome = Fasta(args.ref, args.ref_fai)

    with open(args.ref_gene) as ref_gene_file:
        transcripts = read_transcripts(ref_gene_file)

    cds = {}
    with open(args.trans_cds, 'r') as fp:
        for line in fp.readlines():
            obj = json.loads(line)
            cds[obj['id']] = {'strand': obj['strand'], 'cds': obj['cds'], 'chr': obj['chr']}

    nm_to_ens = {}
    if not os.path.exists(args.ens_to_nm):
        print('--ens_to_nm not specified, use genomics/data/Ens_to_NM.tab')
        pkg = importlib_resources.files('genomics')
        pkg_data_file = pkg / 'data' / 'Ens_to_NM.tab'
        with pkg_data_file.open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            for row in reader:
                ens = row[0]
                nm = row[1]
                nm_to_ens[nm] = ens
    else:
        with open(args.ens_to_nm, 'r') as fp:
            reader = csv.reader(fp, delimiter='\t')
            for row in reader:
                ens = row[0]
                nm = row[1]
                nm_to_ens[nm] = ens

    return genome, transcripts, cds, nm_to_ens


def gen_ref_gene(args):
    # https://github.com/counsyl/hgvs/issues/26
    conn = mysql.connector.connect(
        host='genome-mysql.cse.ucsc.edu',
        user='genomep',
        password='password',
    )
    cursor = conn.cursor()

    cursor.execute("USE hg19;")

    cmd = "SELECT r.bin, " \
          "CONCAT(r.name, '.', g.version) AS name, " \
          "r.chrom," \
          "r.strand," \
          "r.txStart," \
          "r.txEnd," \
          "r.cdsStart," \
          "r.cdsEnd," \
          "r.exonCount," \
          "r.exonStarts," \
          "r.exonEnds," \
          "r.score," \
          "r.name2," \
          "r.cdsStartStat," \
          "r.cdsEndStat," \
          "r.exonFrames " \
          "FROM hg19.refGene r, hgFixed.gbCdnaInfo g " \
          "WHERE r.name = g.acc AND r.chrom NOT LIKE '%\_%' AND r.chrom NOT LIKE '%-%'"

    cursor.execute(cmd)

    result = cursor.fetchall()
    with open(args.output, 'w') as fp:
        writer = csv.writer(fp, delimiter='\t')
        for row in result:
            writer.writerow(map(lambda i: str(i, 'UTF-8') if type(i) is bytes else i, row))


def gen_cds(args):
    parse_transcript_cds(args.gen_code, args.ref, args.output)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_batch = subparsers.add_parser('batch', help='Batch process')
    parser_batch.add_argument('-i',
                              '--input_dir',
                              required=True,
                              type=str,
                              help='Root folder for all reports')
    parser_batch.add_argument('-o',
                              '--output_dir',
                              required=True,
                              type=str,
                              help='Output folder path')
    parser_batch.add_argument('--ref',
                              type=str,
                              help='Ref path')
    parser_batch.add_argument('--ref_fai',
                              type=str,
                              help='Ref index path')
    parser_batch.add_argument('-m',
                              '--maf',
                              action='store_true',
                              help='Generate MAF info')
    parser_batch.add_argument('-v',
                              '--vcf',
                              action='store_true',
                              help='Generate VCF file')
    parser_batch.add_argument('--ref_gene',
                              type=str,
                              default='src/genomics/data/genes.refGene',
                              help='Ref gene path, could be generated by gen-ref-gene sub-command')
    parser_batch.add_argument('--trans_cds',
                              type=str,
                              default='src/genomics/data/transcript_cds.json',
                              help='Transcript CDS, could be generated by gen-cds sub-command')
    parser_batch.add_argument('--ens_to_nm',
                              type=str,
                              default='src/genomics/data/Ens_to_NM.tab',
                              help='Mapping from Ens ID to NM number(first column is Ens ID, second is NM number)')
    parser_batch.set_defaults(func=batch)

    parser_single = subparsers.add_parser('single', help='Process single report')
    parser_single.add_argument('-i',
                               '--input_dir',
                               required=True,
                               type=str,
                               help='PDF folder path')
    parser_single.add_argument('-o',
                               '--output_dir',
                               required=True,
                               type=str,
                               help='Output folder path')
    parser_single.add_argument('-p',
                               '--pid',
                               required=True,
                               type=str,
                               help='Patient ID')
    parser_single.add_argument('--ref',
                               type=str,
                               help='Ref path')
    parser_single.add_argument('--ref_fai',
                               type=str,
                               help='Ref index path')
    parser_single.add_argument('-m',
                               '--maf',
                               action='store_true',
                               help='Generate MAF info')
    parser_single.add_argument('-v',
                               '--vcf',
                               action='store_true',
                               help='Generate VCF file')
    parser_single.add_argument('--ref_gene',
                               type=str,
                               default='src/genomics/data/genes.refGene',
                               help='Ref gene path, could be generated by gen-ref-gene sub-command')
    parser_single.add_argument('--trans_cds',
                               type=str,
                               default='src/genomics/data/transcript_cds.json',
                               help='Transcript CDS, could be generated by gen-cds sub-command')
    parser_single.add_argument('--ens_to_nm',
                               type=str,
                               default='src/genomics/data/Ens_to_NM.tab',
                               help='Mapping from Ens ID to NM number(first column is Ens ID, second is NM number)')
    parser_single.set_defaults(func=single)

    parser_gen_ref_gene = subparsers.add_parser('gen-ref-gene', help='Generate genes.refGene')
    parser_gen_ref_gene.set_defaults(func=gen_ref_gene)
    parser_gen_ref_gene.add_argument('--output',
                                     required=True,
                                     default='./resources/genes.refGene',
                                     help='Ref gene path')

    parser_gen_cds = subparsers.add_parser('gen-cds', help='Generate transcript CDS')
    parser_gen_cds.set_defaults(func=gen_cds)
    parser_gen_cds.add_argument('--output',
                                required=True,
                                default='./resources/transcript_cds.json',
                                help='Transcript CDS path')
    parser_gen_cds.add_argument('--gen_code',
                                required=True,
                                help='Gencode path')
    parser_gen_cds.add_argument('--ref',
                                default='./hg19.fa',
                                help='Ref path')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)
    else:
        args.func(args)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
