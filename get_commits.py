#Usage: $ python3 get_commits.py /home/kevin/Desktop/eclipse-platform

# Given a folder containing one or more git repos, this script will
# extract every commit of each of the repos and generate an xml file
# for each commit in a ./output/REPO_NAME/ folder. It will also generate
# an xml for each project that contains all of that project's commits in a
# ./output/ folder.

__author__ = 'kevin'

from pygit2 import Repository
from lxml import etree
import sys
import os
from datetime import datetime

output_root_path = "./output/"
output_commit_file = "commits.xml"
git_folder = ".git/"

bug_date_format = "%Y-%m-%d %H:%M:%S"
bug_related_words = ["bug", "fix", "defect", "broken", "crash", "freeze", "break", "wrong", "glitch", "proper"]

def commit_to_xml(commit):
    commit_elem = etree.Element("commit",
                                id = str(commit.id),
                                time = str(commit.commit_time),
                                pretty_time = str(datetime.fromtimestamp(commit.commit_time)))
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
    try:
        os.makedirs(output_root_path)
    except FileExistsError as ex:
        pass

    for git_repo in get_immediate_subdirectories(repos_root):
        repo = Repository(os.path.join(git_repo, git_folder))
        root = etree.Element("commits")

        repo_name = os.path.basename(os.path.normpath(git_repo))
        #output_path = os.path.join(output_root_path, repo_name)

        #os.makedirs(output_path)

        for commit in repo.walk(repo.head.target):
            commit_xml = commit_to_xml(commit)

            root.append(commit_xml)

            for e in commit.tree:
                print(e.name)

            # output_single_commit_file_path = os.path.join(output_path, str(commit.id) + ".xml")

            # with open(output_single_commit_file_path, "w") as file:
            #     file.write(xml_to_string(commit_xml))

            #print("> project: " + repo_name + ", commit: " + str(commit.id) + " extracted")

        output_xml = xml_to_string(root)

        with open(os.path.join(output_root_path, repo_name + "_" + output_commit_file), "w") as file:
            file.write(output_xml)

        print("> project: " + repo_name + " extraction finished")


def main():
    extract_commits(sys.argv[1])

if __name__ == "__main__":
    main()
