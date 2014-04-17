# Usage: $ python3 merge_files.py /home/kevin/Desktop/sac-data/contrib-facebook-android-sdk/highest_contributions.csv /home/kevin/Desktop/sac-data/bug-commit-facebook-android-sdk/bug_commit_ratio.csv /home/kevin/Desktop/sac-data/metrics-facebook-android-sdk/metrics.csv output.csv
#
# Merges two given contrib and git_commit files.
# TODO: need to include Metrics

__author__ = 'kevin'

import sys
import csv

csv_header = ['file_name',
              'lines_count',
              'top_single_dev_contribution_knowledge',
              'top_single_dev_contribution_knowledge_percent',
              'commit_num',
              'bug_commit_num',
              'bug_commit_ratio',
              'CountLine',
              'CountLineCode',
              'CountLineComment',
              'SumCyclomatic']


def merge_files(contrib_file, bug_commit_file, metrics_file, output_file):
    with open(contrib_file, "r") as contrib_file:
        # file_name,lines_count,top_single_dev_contribution_knowledge,top_single_dev_contribution_knowledge_percent
        contrib_reader = [row for row in csv.DictReader(contrib_file)]

    with open(bug_commit_file, "r") as bug_commit_file:
        # file_name,commit_num,bug_commit_num,bug_commit_ratio
        bug_commit_reader = [row for row in csv.DictReader(bug_commit_file)]

    with open(metrics_file, "r") as metrics_file:
        # Kind,Name,CountLine,CountLineCode,CountLineComment,SumCyclomatic,Cyclomatic,CountDeclFunction,CountDeclFile
        metrics_reader = [row for row in csv.DictReader(metrics_file)]

    with open(output_file, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, csv_header)
        writer.writeheader()

        # The driver of the iteration needs to be this one because it has only the files
        # "interesting to Git By A Bus". contrib files have less rows than bug-commit and metric files.
        for contrib_row in contrib_reader:
            file_name = contrib_row['file_name']
            file_name = file_name[file_name.index(":") + 1:]  # to clean the file_name

            bug_commit_row = [row for row in bug_commit_reader if row['file_name'] == file_name]
            metric_row = [row for row in metrics_reader if row['Name'] == file_name]

            if not metric_row:
                metric_row = [row for row in metrics_reader
                              if row["Name"][row["Name"].index("/") + 1:] == file_name]

            if bug_commit_row:
                bug_commit_row = bug_commit_row[0]
            else:
                bug_commit_row = {'commit_num': "",
                                  'bug_commit_num': "",
                                  'bug_commit_ratio': ""}

            if metric_row:
                metric_row = metric_row[0]
            else:
                metric_row = {'CountLine': "",
                              'CountLineCode': "",
                              'CountLineComment': "",
                              'SumCyclomatic': ""}

            writer.writerow({'file_name': file_name,
                             'lines_count': contrib_row['lines_count'],
                             'top_single_dev_contribution_knowledge': contrib_row['top_single_dev_contribution_knowledge'],
                             'top_single_dev_contribution_knowledge_percent': contrib_row['top_single_dev_contribution_knowledge_percent'],
                             'commit_num': bug_commit_row['commit_num'],
                             'bug_commit_num': bug_commit_row['bug_commit_num'],
                             'bug_commit_ratio': bug_commit_row['bug_commit_ratio'],
                             'CountLine': metric_row['CountLine'],
                             'CountLineCode': metric_row['CountLineCode'],
                             'CountLineComment': metric_row['CountLineComment'],
                             'SumCyclomatic': metric_row['SumCyclomatic']})


def main():
    contrib_file = sys.argv[1]
    bug_commit_file = sys.argv[2]
    metrics_file = sys.argv[3]
    output_file = sys.argv[4]

    merge_files(contrib_file, bug_commit_file, metrics_file, output_file)


if __name__ == "__main__":
    main()