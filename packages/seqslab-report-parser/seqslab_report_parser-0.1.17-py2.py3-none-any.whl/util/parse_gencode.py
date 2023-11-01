# Purpose: get genomic locations
# Workspace: anome@anome-192-168-188-8:/dbsource/user/gencode/anome_processed
# Author: Chun-Pei Cheng
# Date: 20151223
# Change: [20160601 Allen] Add parsing CDS sequences from gencode and refseq

from optparse import OptionParser
from Bio import SeqIO
from Bio.Seq import Seq
import codecs
import re
import sys
import json

DATA_SOURCE = {'HAVANA', 'ENSEMBL'}


def dump_transcript_cds(transcript, refseq):
    for tid in sorted(transcript.keys()):
        if len(transcript[tid]) == 0:
            continue

        cds = transcript[tid]

        if cds[0]['strand'] == '+':
            cds.sort(key=lambda x: x['exon_number'])
        else:
            cds.sort(key=lambda x: -x['exon_number'])

        record = {
            'id': tid,
            'strand': cds[0]['strand'] == '+',
            'cds': [],
            'cdna': ''
        }

        for c in cds:
            record['cdna'] += str(refseq[c['start'] - 1:c['end']].seq.upper())
            record['cds'].append({
                'start': c['start'],
                'end': c['end'],
                'exon': c['exon_number']
            })

        if len(record['cdna']) % 3 != 0:
            print("coding sequence is not the length of 3.")
            print(str(record))
            continue

        if record['strand'] is False:
            record['cdna'] = str(Seq(record['cdna']).reverse_complement())

        yield record


def parse_transcript_cds(gencode_file, fasta, output_file):
    """
    seqname - name of the chromosome or scaffold; chromosome names can be given with or without the 'chr' prefix.
    source - name of the program that generated this feature, or the data source (database or project name)
    feature - feature type name, e.g. Gene, Variation, Similarity
    start - Start position of the feature, with sequence numbering starting at 1.
    end - End position of the feature, with sequence numbering starting at 1.
    score - A floating point value.
    strand - defined as + (forward) or - (reverse).
    phase - One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base of a codon,
            '1' that the second base is the first base of a codon, and so on..
    attribute - A semicolon-separated list of tag-value pairs, providing additional information about each feature.
    :param gencode_file:
    :param refseq_dir:
    :param output_json:
    :return:
    """
    refseq = SeqIO.index(fasta, "fasta")
    fp = open(output_file, mode='w')

    chromosome = "chr1"
    transcript = {}
    results = []
    for line in open(gencode_file).readlines():
        if line.startswith('#'):
            continue

        seqname, source, feature, start, end, score, strand, phase, attribute = line.strip().split("\t")

        if source not in DATA_SOURCE or (feature != "CDS" and feature != "stop_codon"):
            continue

        if seqname != chromosome:
            # start with new chromosome
            for record in dump_transcript_cds(transcript, refseq[chromosome]):
                record['chr'] = chromosome
                fp.write(json.dumps(record) + '\n')

            # reset variables for new chromosome
            chromosome = seqname
            transcript = {}

        transcript_id = ''
        exon_number = 0

        for item in attribute.strip().split(';'):
            keyvalue = item.strip().split('=')
            if len(keyvalue) == 2:
                if keyvalue[0] == "transcript_id":
                    transcript_id = keyvalue[1].strip("\"")
                    if '_' in transcript_id:
                        transcript_id = transcript_id.split("_")[0]
                elif keyvalue[0] == "exon_number":
                    exon_number = int(keyvalue[1].strip())
                    if feature == "stop_codon":
                        exon_number += 1

        if transcript_id.startswith("ENSTR"):
            continue

        if transcript_id not in transcript:
            transcript[transcript_id] = []

        transcript[transcript_id].append({
            'exon_number': exon_number,
            'start': int(start),
            'end': int(end),
            'strand': strand
        })

    for record in dump_transcript_cds(transcript, refseq[chromosome]):
        record['chr'] = chromosome
        fp.write(json.dumps(record) + '\n')

    refseq.close()
    fp.close()


def parse_genomic_regions(file_path):
    for line in codecs.open(file_path, 'r').readlines():
        if '#' not in line:
            line_split = line.strip().split("\t")
            chr = line_split[0].replace("chr", "")
            type = line_split[2]
            start = int(line_split[3])
            end = int(line_split[4])
            strand = line_split[6]
            info = line_split[8]

            if "gene" == type:
                print("gene\t%s\t%s\t%s" % (chr, start - 5000 if (0 < start - 5000) else 1, end + 5000))

                ensemblID = re.search(r'(E.*)(\.)', info.split(";")[0]).group(1)
                print("%s\t%s\t%s\t%s" % (ensemblID, chr, start - 5000 if (0 < start - 5000) else 1, end + 5000))

                if "+" == strand:
                    print("promoter\t%s\t%s\t%s" % (chr, start - 2000 if (0 < start - 2000) else 1, start))
                    print("upstream\t%s\t%s\t%s" % (chr, start - 5000 if (0 < start - 5000) else 1, start))
                    print("downstream\t%s\t%s\t%s" % (chr, end, end + 5000))

                elif "-" == strand:
                    print("promoter\t%s\t%s\t%s" % (chr, end, end + 2000))
                    print("upstream\t%s\t%s\t%s" % (chr, end, end + 5000))
                    print("downstream\t%s\t%s\t%s" % (chr, start - 5000 if (0 < start - 5000) else 1, start))

            if "CDS" == type:
                print("coding\t%s\t%s\t%s" % (chr, start, end))

            if "exon" == type:
                print("exon\t%s\t%s\t%s" % (chr, start, end))

            if "transcript" == type:
                print("transcript\t%s\t%s\t%s" % (chr, start, end))

            if "start_codon" == type:
                print("start_codon\t%s\t%s\t%s" % (chr, start, end))

            if "stop_codon" == type:
                print("stop_codon\t%s\t%s\t%s" % (chr, start, end))

            if "UTR" == type:
                print("utr\t%s\t%s\t%s" % (chr, start, end))


##########################################################################
# main program
##########################################################################
def main():
    optparser = OptionParser(version="%prog 1.0", usage="%prog -a {region|cds} [options] GENCODE_GTF_FILE")
    optparser.add_option("-a", "--action",
                         dest="action",
                         default="region",
                         help="Action to perform on Gencode: 'regions' or 'cds' [default: %default]")
    optparser.add_option("-f", "--fasta",
                         dest="fasta",
                         default="genome.fa",
                         help="Gencode genome sequence assembly file [default: %default]",
                         metavar="FILE")
    optparser.add_option("-o", "--output",
                         dest="output_file",
                         default="output.json",
                         help="Output json file describing CDS sequences [default: %default]",
                         metavar="FILE")
    (opts, args) = optparser.parse_args()

    if len(args) == 0:
        optparser.print_help(sys.stdout)
        print("please specify Gencode GTF file")
        sys.exit(-1)

    opts.gtf_file = args[0]

    if opts.action == 'region':
        parse_genomic_regions(opts.gtf_file)
    elif opts.action == 'cds':
        parse_transcript_cds(opts.gtf_file, opts.fasta, opts.output_file)
    else:
        optparser.print_help(sys.stdout)
        print("Unknown action!")


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        print("*** Python 3 or above required\n")
        sys.exit(-1)
    main()
