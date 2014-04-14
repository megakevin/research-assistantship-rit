#Usage: $ python3 get_commits.py /home/kevin/Desktop/eclipse-platform ./output/
# python3 get_commits.py <git_repos_path> <output_path>
#
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
from subprocess import check_output

default_output_root_path = "./output/"
output_commit_file = "commits.xml"
git_folder = ".git/"


def commit_to_xml(commit, stats):
    commit_elem = etree.Element("commit",
                                id = str(commit.id),
                                time = str(commit.commit_time),
                                pretty_time = str(datetime.fromtimestamp(commit.commit_time)))
    commit_elem.append(etree.Element("author", name = commit.author.name, email = commit.author.email))
    commit_elem.append(etree.Element("committer", name = commit.committer.name, email = commit.committer.email))

    message_elem = etree.Element("message")
    try:
        message_elem.text = commit.message
    except Exception as ex:
        translation_map = dict.fromkeys(range(32))
        message_elem.text = commit.message.translate(translation_map)

    stats_elem = etree.Element("stats")
    stats_elem.text = stats

    commit_elem.append(message_elem)
    commit_elem.append(stats_elem)

    return commit_elem


def xml_to_string(xml):
    return etree.tostring(xml, pretty_print=True).decode("utf-8")


def get_immediate_subdirectories(root_dir):
    return [os.path.join(root_dir, name) for name in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, name))]


def get_commit_stats(commit_id):
    # This git command returns:
    # "\n
    # <added_lines>\t<deleted_lines>\t<file_name>\n
    # <added_lines>\t<deleted_lines>\t<file_name>"
    cmd_show_numstat = "git show --numstat --format='format:' {0}".format(str(commit_id))
    commit_stats = check_output(cmd_show_numstat, shell=True).decode("utf-8")

    parsed_stats = "\n"

    for file_stats in commit_stats.split("\n"):
        if len(file_stats.split("\t")) == 3:  # Process only if it's a line with actual data
            added_lines, deleted_lines, file_name = file_stats.split("\t")
            parsed_stats += "{0}\t{1}\t{2}\n".format(file_name, added_lines, deleted_lines)

    return parsed_stats


def extract_commits(repos_root, output_path):
    # Uncomment code to generate a separate file for each commit.

    try:
        os.makedirs(output_path)
    except FileExistsError as ex:
        pass

    exec_dir = os.getcwd()

    for git_repo in get_immediate_subdirectories(repos_root):
        os.chdir(git_repo)
        repo = Repository(os.path.join(git_repo, git_folder))
        root = etree.Element("commits")

        repo_name = os.path.basename(os.path.normpath(git_repo))

        print("\n> project: " + repo_name + " extraction started")

        for commit in repo.walk(repo.head.target):
            stats = get_commit_stats(commit.id)
            commit_xml = commit_to_xml(commit, stats)
            root.append(commit_xml)

            # print(".", end=" ")
            print("> project: " + repo_name + ", commit " + str(commit.id) + " processed")

        output_xml = xml_to_string(root)

        os.chdir(exec_dir)

        with open(os.path.join(output_path, repo_name + "_" + output_commit_file), "w") as file:
            file.write(output_xml)

        print("\n> project: " + repo_name + " extraction finished")


def main():

    repo_path = sys.argv[1]
    output_root_path = default_output_root_path

    if len(sys.argv) > 2:
        output_root_path = sys.argv[2]

    extract_commits(repo_path, output_root_path)

if __name__ == "__main__":
    main()
