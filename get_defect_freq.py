# Usage: $ python3 get_comment_ratio.py /home/kevin/Desktop/sac-data/stats output.csv
#          python3 get_comment_ratio.py <merged_files> <output_path>
#
# Merges all the extracted contribution per tag data into one single file.

__author__ = 'kevin'

import sys
import csv
import os

# RQ 1: Generate a csv file for each project with: file, release, if its SAC, LOC
csv_header = ['project',
              'mean SAC', 'mean non SAC', "mean change",
              'pVal']


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
                      'bug_commit_ratio': float(row['bug_commit_ratio']) if row['bug_commit_ratio'] else 0}
                    for row in csv.DictReader(csv_file)]

            files_sac = [{'bug_commit_ratio': l['bug_commit_ratio']}
                         for l in data if l['contrib_percent'] >= 90]
            files_non_sac = [{'bug_commit_ratio': l['bug_commit_ratio']}
                             for l in data if l['contrib_percent'] < 90]

            bug_ratios_sac = [f['bug_commit_ratio'] * 100 for f in files_sac]
            bug_ratios_non_sac = [f['bug_commit_ratio'] * 100 for f in files_non_sac]

            mean_sac = mean(bug_ratios_sac)
            mean_non_sac = mean(bug_ratios_non_sac)

            mean_change = mean_non_sac - mean_sac

        result.append({
            'project': data_file,
            'mean SAC': mean_sac,
            'mean non SAC': mean_non_sac,
            'mean change': mean_change,
            'pVal': "TO CALCULATE"
        })

    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    main(sys.argv)
