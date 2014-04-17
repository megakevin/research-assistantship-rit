# Usage: $ python3 get_metrics.py /home/kevin/Desktop/repos/facebook-android-sdk /home/kevin/Desktop/sac-data/metrics-facebook-android-sdk
# python3 get_metrics.py <git_repo_path> <output_path>
# <output_path> must not contain an ending / and should be the form /metrics-<project_name>

__author__ = 'kevin'

import sys
import os
import csv
from subprocess import check_output, call

default_output_path = "./output/"
default_udb = "project_metrics"
output_file = "metrics.csv"

def get_metrics(git_repo, output_path, udb_name):
    try:
        os.makedirs(output_path)
    except FileExistsError as ex:
        pass

    check_output("export PATH=$PATH:/home/kevin/scitools/bin/linux64", shell=True)

    os.chdir(output_path)

    # Create the metrics-db
    print('> Creating the understand-db')
    check_output("und create -db " + udb_name + " -languages c++ java c# web python add " + git_repo, shell=True)

    # Setup the settings
    check_output("und -db " + udb_name + " settings -Metrics CountLine CountLineCode CountLineComment SumCyclomatic Cyclomatic CountDeclFunction CountDeclFile", shell=True)
    check_output('und -db ' + udb_name + ' settings -ReportReports "File Average Metrics" "Project Metrics" "File Metrics"', shell=True)
    check_output("und -db " + udb_name + " settings -MetricFileNameDisplayMode RelativePath", shell=True)

    # Analyze the code
    print('> Analyzing the code')
    check_output("und -db " + udb_name + " analyze", shell=True)

    # Create the csv file with the metrics
    print('> Getting the metrics')
    check_output("und -db " + udb_name + " metrics", shell=True)

    print('> Storing the metrics into ' + output_path)
    check_output('echo "Kind,Name,CountLine,CountLineCode,CountLineComment,SumCyclomatic,Cyclomatic,CountDeclFunction,CountDeclFile" > ' + os.path.join(output_path, output_file), shell=True)
    check_output('grep "File," ' + udb_name + '.csv' + ' >> ' + os.path.join(output_path, output_file), shell=True)


def main():
    repo_path = sys.argv[1]
    output_path = default_output_path
    udb_name = default_udb

    if len(sys.argv) > 2:
        output_path = sys.argv[2]
        udb_name = os.path.basename(os.path.normpath(output_path))
        udb_name = udb_name[udb_name.index("-") + 1:]
        print(udb_name)

    get_metrics(repo_path, output_path, udb_name)


if __name__ == "__main__":
    main()