# Usage: $ python3 get_sac_files_lines.py /home/kevin/Desktop/sac-data/stats output.csv
#          python3 get_sac_files_lines.py <merged_files> <merged_files> <output_path>
#
# Merges all the extracted contribution per tag data into one single file.

__author__ = 'kevin'

import sys
import csv
import os

# RQ 1: Generate a csv file for each project with: file, release, if its SAC, LOC
csv_header = ['project',
              '70% lines', '70% files',
              '80% lines', '80% files',
              '90% lines', '90% files']

def main(argv):

    data_dir = argv[1]
    output_file = argv[2]

    result = []

    for data_file in os.listdir(data_dir):
        with open(os.path.join(data_dir, data_file), newline="") as csv_file:
            data = [{ 'contrib_percent': float(row['top_single_dev_contribution_knowledge_percent']),
                      'lines': float(row['lines_count'])} for row in csv.DictReader(csv_file)]

            total_lines = sum([f['lines'] for f in data])
            total_files = len(data)

        result.append({
            'project': data_file,
            '70% lines': (sum([f['lines'] for f in data if f['contrib_percent'] >= 70 ]) / total_lines) * 100,
            '70% files': (len([f for f in data if f['contrib_percent'] >= 70 ]) / total_files) * 100,
            '80% lines': (sum([f['lines'] for f in data if f['contrib_percent'] >= 80 ]) / total_lines) * 100,
            '80% files': (len([f for f in data if f['contrib_percent'] >= 80 ]) / total_files) * 100,
            '90% lines': (sum([f['lines'] for f in data if f['contrib_percent'] >= 90 ]) / total_lines) * 100,
            '90% files': (len([f for f in data if f['contrib_percent'] >= 90 ]) / total_files) * 100,
        })

    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    main(sys.argv)
