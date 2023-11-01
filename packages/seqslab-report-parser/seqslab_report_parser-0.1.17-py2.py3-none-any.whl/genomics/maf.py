from typing import Dict, List
import os
import re

from parser.const import *
from genomics.variant import Variant


class MAF(Variant):
    @staticmethod
    def create_maf_meta(dst: str, study_id: str, description: str):
        content = f'cancer_study_identifier: {study_id}\n' \
                  'genetic_alteration_type: MUTATION_EXTENDED\n' \
                  'datatype: MAF\n' \
                  'stable_id: mutations\n' \
                  'show_profile_in_analysis_tab: true\n' \
                  f'profile_description: {description}\n' \
                  'profile_name: Mutations\n' \
                  'data_filename: data_mutations.txt'

        with open(os.path.join(dst, 'meta_mutations.txt'), "w") as file:
            file.write(content)

    @staticmethod
    def create_maf_data_header() -> str:
        content = 'Hugo_Symbol\t' \
                  'NCBI_Build\t' \
                  'Chromosome\t' \
                  'Start_Position\t' \
                  'End_Position\t' \
                  'Strand\t' \
                  'Variant_Classification\t' \
                  'Variant_Type\t' \
                  'Reference_Allele\t' \
                  'Tumor_Seq_Allele1\t' \
                  'Tumor_Seq_Allele2\t' \
                  'Tumor_Sample_Barcode\t' \
                  'Mutation_Status\t' \
                  'HGVSp_Short\t' \
                  'RefSeq'

        return content

    # TODO:
    # A simple converter from amino acid change to variant classification
    # cannot handle following classes:
    # In_Frame_Del, In_Frame_Ins,
    # Translation_Start_Site,
    # Nonstop_Mutation, Targeted_Region
    @staticmethod
    def get_variant_class(amino_acid_change: str, transcript_id: str, variant_type: str, sample_id: str) -> str:
        if transcript_id.startswith('NR_'):
            return 'RNA'

        pattern = r'(p\.)?([A-Za-z\*])(\d+)([A-Za-z\*])'
        match = re.search(pattern, amino_acid_change)
        if match:
            original_aa = match.group(2)
            position = match.group(3)
            new_aa = match.group(4)

            # Check for different variant classifications
            if new_aa == '*':
                return 'Nonsense_Mutation'
            elif new_aa == '=':
                # return 'Synonymous_Mutation'
                return 'Silent'
            elif original_aa != new_aa:
                return 'Missense_Mutation'
            elif 'fs' in amino_acid_change and variant_type == 'INS':
                return 'Frame_Shift_Ins'
            elif 'fs' in amino_acid_change and variant_type == 'DEL':
                return 'Frame_Shift_Del'
            elif 'splice' in amino_acid_change.lower():
                return 'Splice_Site'
        else:
            if 'splice' in amino_acid_change.lower():
                return 'Splice_Site'
            elif 'frameshift' in amino_acid_change.lower():
                return 'Frame_Shift'
            else:
                print(f'Unknown variant class: {sample_id} {amino_acid_change}')
                return '.'

    @staticmethod
    def get_variant_type(
            start: int,
            end: int,
            ref: str,
            tumor_seq_1: str,
            tumor_seq_2: str,
            transcript_id: str,
            sample_id: str) -> str:
        if transcript_id.startswith('NR_') and start == end:
            return 'SNP'

        if not start or not end or ref == '.' or tumor_seq_2 == '.':
            print(f'Unknown variant type: {sample_id} {start}:{end} [{ref}], [{tumor_seq_1}], [{tumor_seq_2}]')
            return '.'

        elif end - start + 1 == len(ref) or end - start == 1 and len(ref) <= len(tumor_seq_2):
            return 'INS'
        elif end - start + 1 == len(ref) and len(ref) >= len(tumor_seq_2):
            return 'DEL'
        elif len(ref) == 1 and len(tumor_seq_1) == 1 and len(tumor_seq_2) == 1 and \
                ref != '-' and tumor_seq_1 != '-' and tumor_seq_2 != '-':
            return 'SNP'
        elif len(ref) == 2 and len(tumor_seq_1) == 2 and len(tumor_seq_2) == 2 and \
                ref != '-' and tumor_seq_1 != '-' and tumor_seq_2 != '-':
            return 'DNP'
        elif len(ref) == 3 and len(tumor_seq_1) == 3 and len(tumor_seq_2) == 3 and \
                ref != '-' and tumor_seq_1 != '-' and tumor_seq_2 != '-':
            return 'TNP'
        elif len(ref) > 3 and len(tumor_seq_1) > 3 and len(tumor_seq_2) > 3 and \
                ref != '-' and tumor_seq_1 != '-' and tumor_seq_2 != '-':
            return 'ONP'
        else:
            print(f'Unknown variant type: {sample_id} {start}:{end} [{ref}], [{tumor_seq_1}], [{tumor_seq_2}]')
            return '.'

    def to_maf(self, sample_id: str, variant_info: List[Dict[str, List[str]]]) -> List[Dict[str, str]]:
        maf = []
        for info in variant_info:
            transcript_id = self.to_str(info[VARIANT_ACCESSION])
            cdna = self.normalize_cdna(''.join(info.get(VARIANT_HGVS, [''])))
            locus = self.to_str(info.get(VARIANT_POSITION, ['.']))
            chrom, start, ref, alt = self.parse_hgvs_name(transcript_id, cdna, locus)
            end = self.get_end_position(start, ref, transcript_id)
            aac = self.to_str(info[VARIANT_AMINO_ACID_CHANGE])
            variant_type = MAF.get_variant_type(start, end, ref, ref, alt, transcript_id, sample_id)
            variant_class = self.to_str(info[VARIANT_EFFECT]) if VARIANT_EFFECT in info \
                else MAF.get_variant_class(aac, transcript_id, variant_type, sample_id)
            m = {
                'Hugo_Symbol': self.to_str(info[GENE]),
                'NCBI_Build': 'GRCH37',
                'Chromosome': self.normalize_chrom(self.to_str(info.get(CHROMOSOME, [chrom]))),
                'Start_Position': start,
                'End_Position': end,
                'Strand': '+',
                'Variant_Classification': variant_class,
                'Variant_Type': variant_type,
                'Reference_Allele': ref,
                'Tumor_Seq_Allele1': ref,
                'Tumor_Seq_Allele2': alt,
                'Tumor_Sample_Barcode': sample_id,
                'Mutation_Status': 'Somatic',
                'HGVSp_Short': aac,
                'RefSeq': self.to_str(info[VARIANT_ACCESSION])
            }
            maf.append(m)

        return maf

    def archer_to_maf(self, sample_id: str, variant_info: List[Dict[str, List[str]]]) -> List[Dict[str, str]]:
        maf = []
        for info in variant_info:
            ref = self.to_str(info[VARIANT_REF])
            alt = self.to_str(info[VARIANT_MUTATION])
            position = self.to_str(info[VARIANT_POSITION]).split(':')
            chrom = position[0][0]
            start = int(position[1][0])
            end = start + len(ref)
            variant_type = ''  # MAF.get_variant_type(start, end, ref, ref, alt, transcript_id, sample_id)
            m = {
                'Hugo_Symbol': self.to_str(info[GENE]),
                'NCBI_Build': 'GRCH37',
                'Chromosome': chrom,
                'Start_Position': start,
                'End_Position': end,
                'Strand': '+',
                'Variant_Classification': self.to_str(info['Mutation_Classification']),
                'Variant_Type': variant_type,
                'Reference_Allele': ref,
                'Tumor_Seq_Allele1': ref,
                'Tumor_Seq_Allele2': alt,
                'Tumor_Sample_Barcode': sample_id,
                'Mutation_Status': 'Somatic',
                'HGVSp_Short': self.to_str(info[VARIANT_AMINO_ACID_CHANGE]),
                'RefSeq': self.to_str(info[VARIANT_ACCESSION])
            }
            maf.append(m)

        return maf
