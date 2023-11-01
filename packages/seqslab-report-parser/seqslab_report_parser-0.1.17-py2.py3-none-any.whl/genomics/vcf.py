from typing import Dict, List
import csv
import os

from Bio import bgzf
from pyfaidx import Fasta
from pyhgvs.models import Transcript

from parser.const import *
from genomics.variant import Variant


class VCF(Variant):
    def __init__(
            self,
            genome: Fasta,
            transcripts: Dict[str, Transcript],
            cds: Dict,
            nm_to_ens: Dict[str, str],
            ref_fa_path: str,
            ref_fa_fai_path: str,
            ref_gene_path: str):
        super().__init__(genome, transcripts, cds, nm_to_ens, ref_fa_path, ref_gene_path)
        self.ref_fa_fai_path = ref_fa_fai_path

    @staticmethod
    def write_vcf(output_dir: str, file_name: str, header: str, vcf: List[Dict[str, str]]):
        with bgzf.open(os.path.join(output_dir, file_name + '.vcf.gz'), 'wt') as fp:
            fp.write(header)
            for v in vcf:
                s = map(lambda i: str(i) if type(i) is int else i, v.values())
                fp.write('\t'.join(s) + '\n')

    @staticmethod
    def create_simple_vcf_header() -> str:
        meta = '##fileformat=VCFv4.3\n' \
               '##source=Report-Parser\n' \
               '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\n'

        return meta

    def create_vcf_header(self, company: str, sample_id: str) -> str:
        contig = ''
        with open(self.ref_fa_fai_path, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                k = row[0]
                v = row[1]
                if '_' not in k:
                    contig += f'##contig=<ID={k},length={v}>\n'

        meta = '##fileformat=VCFv4.3\n' \
               '##source=Report-Parser\n' \
               f'{contig}' \
               f'##INFO=<ID=AF_{company},Number=1,Type=String,Description="Allele Frequency">\n' \
               '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n' \
               f'##reference=file://{self.ref_fa_path}\n' \
               f'#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{sample_id}\n'

        return meta

    def to_vcf(
            self,
            company: str,
            sample_id: str,
            variant_info: List[Dict[str, List[str]]]) -> (str, List[Dict[str, str]]):
        header = self.create_vcf_header(company, sample_id)
        vcf = []
        for info in variant_info:
            transcript_id = self.to_str(info[VARIANT_ACCESSION])
            cdna = self.normalize_cdna(''.join(info.get(VARIANT_HGVS, [''])))
            locus = self.to_str(info.get(VARIANT_POSITION, ['.']))
            af_str = info[VARIANT_ALLELE_FRACTION] if VARIANT_ALLELE_FRACTION in info else info[
                VARIANT_ALLELE_FREQUENCY]
            af = self.normalize_allele_freq(self.to_str(af_str))
            chrom, start, ref, alt = self.parse_hgvs_name(transcript_id, cdna, locus)
            v = {
                'CHROM': self.normalize_chrom(self.to_str(info.get(CHROMOSOME, [chrom]))),
                'POS': start,
                'ID': '.',
                'REF': ref,
                'ALT': alt,
                'QUAL': '.',
                'FILTER': '.',
                'INFO': f'AF_{company}={af}',
                'FORMAT': 'GT',
                f'{sample_id}': './.'
            }
            vcf.append(v)

        return header, vcf

    def archer_to_vcf(
            self,
            company: str,
            sample_id: str,
            variant_info: List[Dict[str, List[str]]]) -> (str, List[Dict[str, str]]):
        header = self.create_vcf_header(company, sample_id)
        vcf = []
        for info in variant_info:
            position = self.to_str(info[VARIANT_POSITION]).split(':')
            chrom = position[0]
            start = position[1]
            v = {
                'CHROM': chrom,
                'POS': start,
                'ID': '.',
                'REF': self.to_str(info[VARIANT_REF]),
                'ALT': self.to_str(info[VARIANT_MUTATION]),
                'QUAL': '.',
                'FILTER': '.',
                'INFO': f'AF_{company}={self.to_str(info[VARIANT_ALLELE_FRACTION])}',
                'FORMAT': 'GT',
                f'{sample_id}': './.'
            }
            vcf.append(v)

        return header, vcf
