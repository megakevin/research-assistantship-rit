#Usage: $ python3 get_bug_commit_ratio_per_file.py /home/kevin/Desktop/repos/facebook-android-sdk ./output/
# python3 get_bug_commit_ratio_per_file.py <git_repo_path> <output_path>

__author__ = 'kevin'

from pygit2 import Repository
import sys
import os
import csv
from subprocess import check_output

default_output_path = "./output/"
output_file = "bug_commit_ratio.csv"
git_folder = ".git/"

csv_header = ['file_name', 'commit_num', 'bug_commit_num', 'bug_commit_ratio']
bug_related_words = ["bug", "fix", "defect", "broken", "crash", "freeze", "break", "wrong", "glitch", "proper"]


def is_bug_related(commit):
    return any([word.upper() in commit.message.upper() for word in bug_related_words])


def get_touched_files(commit):
    # This git command returns:
    # "\n
    # <added_lines>\t<deleted_lines>\t<file_name>\n
    # <added_lines>\t<deleted_lines>\t<file_name>"
    cmd_show_numstat = "git show --numstat --format='format:' {0}".format(str(commit.id))
    commit_stats = check_output(cmd_show_numstat, shell=True).decode("utf-8")

    touched_files = []

    for file_stats in commit_stats.split("\n"):
        if len(file_stats.split("\t")) == 3:  # Process only if it's a line with actual data
            added_lines, deleted_lines, file_name = file_stats.split("\t")
            touched_files.append(file_name)

    return touched_files


def get_bug_commit_ratio_per_file(git_repo, output_path):
    try:
        os.makedirs(output_path)
    except FileExistsError as ex:
        pass

    result = []
    exec_dir = os.getcwd()
    repo = Repository(os.path.join(git_repo, git_folder))

    os.chdir(git_repo)

    for commit in repo.walk(repo.head.target):
        touched_files = get_touched_files(commit)
        bug_related = is_bug_related(commit)

        for file in touched_files:
            file_data = [f for f in result if f['file_name'] == file]

            if file_data:
                file_data = file_data[0]
                file_data['commit_num'] += 1
                if bug_related:
                    file_data['bug_commit_num'] += 1
            else:
                result.append({'file_name': file,
                               'commit_num': 1,
                               'bug_commit_num': 1 if bug_related else 0})

    os.chdir(exec_dir)

    for entry in result:
        entry['bug_commit_ratio'] = entry['bug_commit_num'] / entry['commit_num']

    output_file_path = os.path.join(output_path, output_file)

    with open(output_file_path, "w", newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


def main():
    repo_path = sys.argv[1]
    output_path = default_output_path

    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    get_bug_commit_ratio_per_file(repo_path, output_path)


if __name__ == "__main__":
    main()