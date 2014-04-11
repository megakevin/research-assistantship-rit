#Usage: $ python3 parser.py /home/kevin/Desktop/eclipse-platform /home/kevin/Downloads/eclipse-bugs.csv

__author__ = "kevin"

from pygit2 import Repository
from lxml import etree
import sys
import os
import csv
from datetime import datetime
import re

output_root_path = "./output/"
output_commit_file = "commits.xml"
git_folder = ".git/"

bug_date_format = "%Y-%m-%d %H:%M:%S"
bug_related_words = ["bug", "fix", "defect", "broken", "crash", "freeze", "break", "wrong", "glitch", "proper"]


def commit_to_xml(commit):
    commit_elem = etree.Element("commit", id = str(commit.id), time = str(commit.commit_time))
    commit_elem.append(etree.Element("author", name = commit.author.name, email = commit.author.email))
    commit_elem.append(etree.Element("committer", name = commit.committer.name, email = commit.committer.email))

    message_elem = etree.Element("message")
    message_elem.text = commit.message

    commit_elem.append(message_elem)

    return commit_elem


def xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")


def get_immediate_subdirectories(root_dir):
    return [os.path.join(root_dir, name) for name in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, name))]


# Regex patterns to find bug ids according to http://dl.acm.org/citation.cfm?id=1083147
# bug[# \t]*[0-9]+,
# pr[# \t]*[0-9]+,
# show\_bug\.cgi\?id=[0-9]+, or <--- wtf is this?
# \[[0-9]+\]

def are_related(commit, bug_report):
    related = False

    upper_case_commit_message = commit.message.upper()
    bug_id = bug_report["id"]

    if re.search("BUG[# \s]*" + bug_id + "[ \s]+|" +
                 "BUG[# \s]*" + bug_id + "$" + "|" +
                 "PR[# \s]*" + bug_id + "[ \s]+" + "|" +
                 "PR[# \s]*" + bug_id + "$" + "|" +
                 "[ \s\D]+" + bug_id + "[ \s]+" +
                 "^" + bug_id + "$",
                 upper_case_commit_message):
        related = True

    return related

def is_bug_related(commit):
    return any([word.upper() in commit.message.upper()
                for word in bug_related_words]) or re.search("^[0-9]+$", commit.message)


def cross_reference_commits_with_bug_reports():
    repos_root = sys.argv[1]#"/home/kevin/Desktop/eclipse-platform"#
    bug_reports_file = sys.argv[2]#"/home/kevin/Downloads/eclipse-bugs.csv"#

    with open(bug_reports_file, newline="") as csv_file:
        bug_reports = [{"id": bug["id"],
                        "creation_time": datetime.strptime(bug["creation_time"], bug_date_format),
                        "closed_time": datetime.strptime(bug["closed_time"], bug_date_format)}
                       for bug in csv.DictReader(csv_file)]

    os.makedirs(output_root_path)

    for git_repo in get_immediate_subdirectories(repos_root):
        repo_name = os.path.basename(os.path.normpath(git_repo))
        repo = Repository(os.path.join(git_repo, git_folder))
        bug_related_commits = [commit for commit in repo.walk(repo.head.target) if is_bug_related(commit)]

        root = etree.Element("commits")
        count = 0

        for bug_report in bug_reports:

            # This may actually hurt the detection
            bug_related_commits_within_bug_life = \
                [c for c in bug_related_commits
                 if bug_report['creation_time'] <= datetime.fromtimestamp(c.commit_time) <= bug_report['closed_time']]

            # for commit in bug_related_commits:
            for commit in bug_related_commits_within_bug_life:
                if are_related(commit, bug_report):
                    commit_xml = commit_to_xml(commit)
                    commit_xml.set("related_bug", bug_report["id"])
                    root.append(commit_xml)
                    count += 1

            print("repo: " + repo_name + ", bug: " + bug_report["id"] + " processed")

            # if count > 10:
            #     break

        root.set("count", str(count))
        output_xml = xml_to_string(root)

        with open(os.path.join(output_root_path, repo_name + "_" + output_commit_file), "w") as file:
            file.write(output_xml)


def main():
    cross_reference_commits_with_bug_reports()

if __name__ == "__main__":
    main()
