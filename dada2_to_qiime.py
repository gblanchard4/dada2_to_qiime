#!/usr/bin/env python
import argparse
import numpy as np

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"


def remove_quotes(line):
    line = line.replace('"', '')
    return line


def dict_to_repset(repsetfile, otudict):
    with open(repsetfile, 'w') as outhandle:
        for key in otudict:
            outhandle.write(">{}\n{}\n".format(key, otudict[key]))


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description='Convert a dada2 seqtab to qiime formatted goodies')

    # Input file
    parser.add_argument('-i', '--input', dest='input', required=True, help='The input file')
    # Threads
    parser.add_argument('-t', '--threads', dest='threads', default=8, help='The number of threads to use for QIIME functions')
    # Prefix
    parser.add_argument('-p', '--prefix', dest='prefix', default="SV", help='The prefix for each unique sequence variant i.e SV1')

    # Parse arguments
    args = parser.parse_args()
    seqtab = args.input
    threads = args.threads

    otutable = seqtab + ".otutable"
    rep_set = seqtab + ".repset"
    parsed_lines = []
    with open(seqtab) as seqtab_handle, open(otutable, 'w') as otuhandle:
        for index, line in enumerate(seqtab_handle):
            if index == 0:
                otus = map(remove_quotes, line.rstrip('\n').split(','))[1::]
                otu_dict = {"{}{}".format(prefix,n): seq for n, seq in enumerate(otus)}
                dict_to_repset(rep_set, otu_dict)
                parsed_lines.append(["#OTU ID"]+[prefix+n for n in (map(str, range(0, len(otus))))])
            else:
                parsed_lines.append(remove_quotes(line).rstrip().split(','))

        otuhandle.write('\n'.join(['\t'.join(line) for line in list(np.array(parsed_lines).T)]))

    sh = '''#DADA2 to QIIME Conversion
parallel_align_seqs_pynast.py -i {0} -o pynast_aligned -O {3}
filter_alignment.py -i pynast_aligned/{2}_aligned.fasta  -o pynast_aligned/
make_phylogeny.py -i pynast_aligned/{2}_aligned.fasta  -o tree.tre
parallel_assign_taxonomy_rdp.py -i {0} -o rdp_assigned_taxonomy/ -O {3} 
biom convert -i {1} --to-json -o otus.json --table-type "OTU table"
biom add-metadata -i otus.json -o otus.taxa.json --observation-metadata-fp rdp_assigned_taxonomy/{2}_tax_assignments.txt --observation-header OTUID,taxonomy,confidence,method --sc-separated taxonomy
biom convert -i otus.taxa.json --to-json -o otus.json --table-type "OTU table"
noderize_med_biom.py -i otus.json -o otus.biom
'''.format(rep_set, otutable, seqtab, threads)
    with open('dada_to_qiime.sh', 'w') as script:
        script.write(sh)


if __name__ == '__main__':
    main()
