#Usage: send .git path as a parameter from console

__author__ = "kevin"

from pygit2 import Repository
from lxml import etree
import sys


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


def main():

    git_repo = sys.argv[1]

    repo = Repository(git_repo)
    root = etree.Element("commits")

    for commit in repo.walk(repo.head.target):
        commit_xml = commit_to_xml(commit)

        root.append(commit_xml)

        with open(str(commit.id) + ".xml", "w") as file:
            file.write(xml_to_string(commit_xml))

    output_xml = xml_to_string(root)

    with open("commits.xml", "w") as file:
        file.write(output_xml)


if __name__ == "__main__":
    main()