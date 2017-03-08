#!/usr/bin/env python3
import argparse
import json

__author__ = "Gene Blanchard"
__email__ = "me@geneblanchard.com"


def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description="Add's MED Node information to the BIOM's taxonomic information")

    # Input file
    parser.add_argument('-i', '--input', dest='input', help='The input file')
    # Output file
    parser.add_argument('-o', '--output', dest='output', help='The output file')

    # Parse arguments
    args = parser.parse_args()
    infile = args.input
    outfile = args.output

    taxa_labels = ['k__None', 'p__', 'c__', 'o__', 'f__', 'g__', 's__']
    with open(infile, 'r') as biom, open(outfile, 'w') as nodebiom:
        data = json.load(biom)
        # Try and write a json file out
        nodebiom.write("{\n")
        nodebiom.write('"id":"{}",\n'.format(data['id']))
        nodebiom.write('"format": "{}",\n'.format(data['format']))
        nodebiom.write('"format_url": "{}",\n'.format(data['format_url']))
        nodebiom.write('"type": "{}",\n'.format(data['type']))
        nodebiom.write('"generated_by": "{}",\n'.format(data['generated_by']))
        nodebiom.write('"date": "{}",\n'.format(data['date']))
        for row in data['rows']:
            row_len = len(row['metadata']['taxonomy'])
            if row_len == 7:
                # print(row['metadata']['taxonomy'])
                row['metadata']['taxonomy'].append("n__{}".format(row['id']))
                # print(row['metadata']['taxonomy'])
            else:
                # print(row['metadata']['taxonomy'])
                row['metadata']['taxonomy'] += taxa_labels[row_len::]
                # print(row['metadata']['taxonomy'])
                row['metadata']['taxonomy'].append("n__{}".format(row['id']))
                # print(row['metadata']['taxonomy'])
                # print("-------------------------------------------------")
        nodebiom.write('"rows": {},\n'.format(json.dumps(data['rows'])))
        nodebiom.write('"columns": {},\n'.format(json.dumps(data['columns'])))
        nodebiom.write('"matrix_type": "{}",\n'.format(data['matrix_type']))
        nodebiom.write('"matrix_element_type": "{}",\n'.format(data['matrix_element_type']))
        nodebiom.write('"shape": {},\n'.format(data['shape']))
        nodebiom.write('"data": {}\n'.format(json.dumps(data['data'])))
        nodebiom.write('}\n')

if __name__ == '__main__':
    main()
