from typing import Dict, List
import re

from Bio.Seq import Seq
from pyfaidx import Fasta
from pyhgvs.models import Transcript
import pyhgvs as hgvs


class Variant:

    def __init__(
            self,
            genome: Fasta,
            transcripts: Dict[str, Transcript],
            cds: Dict,
            nm_to_ens: Dict[str, str],
            ref_fa_path: str,
            ref_gene_path: str):
        self.genome = genome
        self.transcripts = transcripts
        self.ref_fa_path = ref_fa_path
        self._ref_gene_path = ref_gene_path
        self._cds = cds
        self._nm_to_ens = nm_to_ens

    def get_transcripts(self, transcript_id: str):
        t = self.transcripts.get(transcript_id)
        if t:
            return t
        else:
            return self.transcripts.get(transcript_id.split('.')[0])

    def parse_hgvs_name(self, transcript_id: str, cdna: str, locus: str) -> (str, int, str, str):
        t = self.get_transcripts(transcript_id)
        chrom = '.'
        start = None
        if locus and locus != '.':
            parsed_locus = locus.split(':')
            chrom = parsed_locus[0]
            start = int(parsed_locus[1])
        ref = '.'
        alt = '.'

        if t:
            try:
                chrom, start, ref, alt = hgvs.parse_hgvs_name(
                    f'{transcript_id}:{cdna}',
                    self.genome,
                    t,
                    get_transcript=lambda i: self.transcripts.get(i))
            except hgvs.InvalidHGVSName:
                if cdna != 'c.' and not transcript_id.startswith('NR'):
                    chrom, start, ref, alt = self.parse_hgvs_name_by_gencode(transcript_id, cdna)
                else:
                    print(f'cannot parse {transcript_id}:{cdna}')
        else:
            print(f'parse_hgvs_name() failed: cannot find {transcript_id} from {self._ref_gene_path}')

        if chrom == '.' or not start:
            raise RuntimeError(f'parse_hgvs_name() failed: {transcript_id}:{cdna}')

        return chrom, start, ref, alt

    def parse_hgvs_name_by_gencode(self, transcript_id: str, cdna: str) -> (str, int, str, str):
        ens = self._nm_to_ens[transcript_id.split('.')[0]]
        cds = self._cds[ens]['cds']
        s, s_offset, e, e_offset = Variant.parse_cdna_position(cdna)
        chrom = self._cds[ens]['chr']
        strand = self._cds[ens]['strand']
        start = self.calculate_position(s, cds.copy(), strand) + s_offset if strand \
            else self.calculate_position(e, cds.copy(), strand) - e_offset
        end = self.calculate_position(e, cds.copy(), strand) + e_offset if strand \
            else self.calculate_position(s, cds.copy(), strand) - s_offset
        ref = self.genome[chrom][start - 1: end].seq
        alt = '.'
        if 'inv' in cdna:
            alt = self.genome[chrom][start - 1: end].reverse.complement.seq
        elif '>' in cdna and strand:
            alt = cdna.split('>')[1]
        elif '>' in cdna and not strand:
            a = cdna.split('>')[1]
            alt = str(Seq(a).complement())
        else:
            raise RuntimeError(f'parse_hgvs_name_by_gencode() failed: {transcript_id}:{cdna}')

        return chrom, start, ref, alt

    @staticmethod
    def parse_cdna_position(cdna: str) -> (int, int, int, int):
        pattern = r'c\.(\d+)([+-]?\d*)_?(\d+)([+-]?\d*)?.*'
        match = re.search(pattern, cdna)
        if match:
            start = int(match.group(1))
            s_offset = int(match.group(2)) if match.group(2) else 0
            end = int(match.group(3))
            e_offset = int(match.group(4)) if match.group(4) else 0
            return start, s_offset, end, e_offset

    @staticmethod
    def calculate_position(position: int, cds, strand: bool):
        if not strand:
            cds.reverse()

        for c in cds:
            interval = c['end'] - c['start'] + 1
            if interval >= position:
                if strand:
                    return c['start'] + position - 1    # 0 base
                else:
                    return c['end'] - position + 1      # 0 base
            else:
                position = position - interval

    @staticmethod
    def get_end_position(start_position: int, ref: str, transcript_id: str) -> int:
        if start_position and transcript_id.startswith('NM_'):
            return start_position + len(ref) - 1
        elif start_position and transcript_id.startswith('NR_'):
            return start_position
        else:
            return None

    @staticmethod
    def normalize_allele_freq(af: str) -> str:
        if af.endswith('%'):
            return str(float(af.strip('%')) / 100.0)
        else:
            return af

    @staticmethod
    def normalize_cdna(cdna: str) -> str:
        normalized = cdna if cdna.startswith('c.') else f'c.{cdna}'
        pattern = r'c\.(\d+[+-]?\d*)_?(\d+[+-]?\d*)?([ACGT]*)>([ACGT]+)'
        match = re.search(pattern, normalized)
        if match:
            start_position = match.group(1)
            end_position = match.group(2)
            original_seq = match.group(3)
            mutated_seq = match.group(4)

            if start_position and end_position and (len(original_seq) > 1 or len(mutated_seq) > 1):
                return f'c.{start_position}_{end_position}delins{mutated_seq}'

        return normalized

    @staticmethod
    def normalize_chrom(chrom: str) -> str:
        if chrom.startswith('chr'):
            return chrom
        else:
            return 'chr' + chrom

    @staticmethod
    def to_str(ls: List[str]) -> str:
        s = ''.join(s for s in ls if not s.startswith('('))
        if s == '':
            return '.'
        else:
            return s
