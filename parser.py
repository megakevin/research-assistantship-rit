#Usage: $ python3 parser.py /home/kevin/Desktop/eclipse-platform /home/kevin/Downloads/eclipse-bugs.csv
# given a folder containing one or more git repos, this script will
# extract every commit of each of the repos and generate an xml file
# for each commit in a ./output/REPO_NAME/ folder. It will also generate
# an xml for each project that contains all of that project's commits in a
# ./output/ folder.

__author__ = "kevin"

from pygit2 import Repository
from lxml import etree
import sys
import os
import csv
from time import strptime, mktime
from datetime import datetime

output_root_path = "./output/"
output_commit_file = "commits.xml"
git_folder = ".git/"

bug_date_format = "%Y-%m-%d %H:%M:%S"
bug_related_words = ["bug"]


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


def extract_commits(repos_root):
    # Uncomment code to generate a separate file for each commit.
    os.makedirs(output_root_path)

    for git_repo in get_immediate_subdirectories(repos_root):
        repo = Repository(os.path.join(git_repo, git_folder))
        root = etree.Element("commits")

        repo_name = os.path.basename(os.path.normpath(git_repo))
        #output_path = os.path.join(output_root_path, repo_name)

        #os.makedirs(output_path)

        for commit in repo.walk(repo.head.target):
            commit_xml = commit_to_xml(commit)

            root.append(commit_xml)

            # output_single_commit_file_path = os.path.join(output_path, str(commit.id) + ".xml")

            # with open(output_single_commit_file_path, "w") as file:
            #     file.write(xml_to_string(commit_xml))

            #print("> project: " + repo_name + ", commit: " + str(commit.id) + " extracted")

        output_xml = xml_to_string(root)

        with open(os.path.join(output_root_path, repo_name + "_" + output_commit_file), "w") as file:
            file.write(output_xml)

        print("> project: " + repo_name + " extraction finished")


def are_related(commit, bug_report):
    related = False

    commit_time = datetime.fromtimestamp(commit.commit_time)

    if bug_report['creation_time'] < commit_time < bug_report['closed_time']:
        if bug_report["id"] in commit.message:
            related = True

    return related

def is_bug_related(commit):
    return any([word in commit.message for word in bug_related_words])


def cross_reference_commits_with_bug_reports():
    repos_root = sys.argv[1]#"/home/kevin/Desktop/eclipse-platform"#
    bug_reports_file = sys.argv[2]#"/home/kevin/Downloads/eclipse-bugs.csv"#

    csv_file = open(bug_reports_file, newline="")
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
            for commit in bug_related_commits:
                if are_related(commit, bug_report):
                    commit_xml = commit_to_xml(commit)
                    commit_xml.set("related_bug", bug_report["id"])
                    root.append(commit_xml)
                    count += 1

            print("repo: " + repo_name + ", bug: " + bug_report["id"] + " processed")

        root.set("count", str(count))
        output_xml = xml_to_string(root)

        with open(os.path.join(output_root_path, repo_name + "_" + output_commit_file), "w") as file:
            file.write(output_xml)

        print("> project: " + repo_name + " extraction finished")


def main():
    #repos_root = sys.argv[1]
    #extract_commits(repos_root)
    cross_reference_commits_with_bug_reports()

if __name__ == "__main__":
    main()
