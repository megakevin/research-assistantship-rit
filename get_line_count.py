# Usage: $ python3 get_line_count.py /home/kevin/Desktop/sac-data/stats output.csv
#          python3 get_line_count.py <merged_files> <output_path>
#
# Merges all the extracted contribution per tag data into one single file.

__author__ = 'kevin'

import sys
import csv
import os

# RQ 1: Generate a csv file for each project with: file, release, if its SAC, LOC
csv_header = ['project',
              'mean SAC', 'mean non SAC', "mean change",
              'median SAC', 'median non SAC', "median change",
              'pVal']

def median(l):
    l = sorted(l)
    if len(l) % 2 == 0:
        n = len(l)//2
        try:
            val = (l[n]+l[n-1])/2
        except Exception as ex:
            print(ex)

        return val
    else:
        return l[len(l)//2]

def mean(l):
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')

def main(argv):

    data_dir = argv[1]
    output_file = argv[2]

    result = []

    for data_file in os.listdir(data_dir):
        with open(os.path.join(data_dir, data_file), newline="") as csv_file:
            #file_name	lines_count	top_single_dev_contribution_knowledge
            # top_single_dev_contribution_knowledge_percent	commit_num	bug_commit_num
            # bug_commit_ratio	CountLine	CountLineCode	CountLineComment	SumCyclomatic

            data = [{ 'contrib_percent': float(row['top_single_dev_contribution_knowledge_percent']),
                      'count_line': float(row['CountLine']) if row['CountLine'] != "" else 0}
                    for row in csv.DictReader(csv_file)]

            files_line_count_sac = [l['count_line'] for l in data if l['contrib_percent'] >= 90]
            files_line_count_non_sac = [l['count_line'] for l in data if l['contrib_percent'] < 90]

            mean_SAC = mean(files_line_count_sac)
            mean_non_SAC = mean(files_line_count_non_sac)

            mean_change = mean_non_SAC - mean_SAC

            median_SAC = median(files_line_count_sac)
            median_non_SAC = median(files_line_count_non_sac)

            median_change = median_non_SAC - median_SAC

        result.append({
            'project': data_file,
            'mean SAC': mean_SAC,
            'mean non SAC': mean_non_SAC,
            'mean change': mean_change,
            'median SAC': median_SAC,
            'median non SAC': median_non_SAC,
            'median change': median_change,
            'pVal': "TO CALCULATE"
        })

    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    main(sys.argv)
