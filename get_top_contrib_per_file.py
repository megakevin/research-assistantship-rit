#Usage: $ python3 get_top_contrib_per_file.py
#         /home/kevin/Desktop/git_by_a_bus/output/estimate_unique_knowledge.tsv
#         ./get_contrib_per_file_output/
#
#         python3 get_top_contrib_per_file.py <unique_knowledge_file> <output_dir>

# Uses the estimate_unique_knowledge.tsv file generated by Git By A Bus to extract
# each file's top contributor and their percentage of unique contribution.

__author__ = 'kevin'

import sys
import os


class Contribution():
    def __init__(self, contrib_tuple):
        self.contributors = contrib_tuple[0]
        self.knowledge = float(contrib_tuple[1])

    def __str__(self):
        return str(self.contributors).strip("[]").replace("'", "") + ":" + str(self.knowledge)


class KnowledgeFileData():
    """
    Encapsulates the data contained in a line of
    the estimate_unique_knowledge.tsv file

    estimate_unique_knowledge.tsv description:

    file structure => file_name \t lines_count \t developer_experience \t total_knowledge \t developer_unique

    total_knowledge => An int, calculated total knowledge represented by the file

    developer_unique => Quantity of the knowledge (total_knowledge) owned by each developer group on the file.
                        Adding every value equals total_knowledge

                        'Chris Lang:Michael Marucheck:2.2077050433,
                        Michael Marucheck:13.359602649,
                        Chris Lang:15.7326923077'

                        [(['Chris Lang', 'Michael Marucheck'], 2.20770504330107),
                        (['Michael Marucheck'], 13.359602649006622),
                        (['Chris Lang'], 15.732692307692307)]

    Attributes:
        int lines_count
        float total_knowledge
        List<Contribution> dev_unique
    """

    def __init__(self, line):
        fields = line.strip("\t\n").split("\t")

        self.file_name, self.lines_count, self.dev_experience, self.total_knowledge, self.dev_unique = fields

        self.lines_count = int(self.lines_count)
        self.total_knowledge = float(self.total_knowledge)
        self.dev_unique = [Contribution(c) for c in self.parse_dev_shared(self.dev_unique)]

    def parse_dev_shared(self, s):
        dev_shared = []
        if not s:
            return dev_shared
        for ddv in s.split(','):
            segs = ddv.split(':')
            k = segs[:-1]
            v = float(segs[-1])
            dev_shared.append((k, v))

        return dev_shared

    def get_top_unique_contribution(self):
        """
            Returns the contribution with the most knowledge (i.e. the biggest contribution)
            made by a single developer to the file this object represents.
        Returns:
            Contribution
        """
        predicate = lambda c: c.knowledge
        top_contribution = max(self.get_unique_contributions(), key=predicate)

        return top_contribution

    def get_unique_contributions(self):
        """
            Returns a list with all the contributions made by a single developer
            to the file this object represents.
        Returns:
            List<Contribution>
        """
        return [contrib for contrib in self.dev_unique if len(contrib.contributors) == 1]

    def get_contribution_percent(self, contribution):

        contribution_percent = 0

        if self.total_knowledge != 0:
            contribution_percent = (contribution.knowledge / self.total_knowledge) * 100

        return contribution_percent

    highest_contribution_header = "file_name,lines_count,top_single_dev_contribution_knowledge,top_single_dev_contribution_knowledge_percent\n"

    def to_highest_contribution_string(self, separator):
        return self.file_name + separator + \
               str(self.lines_count) + separator + \
               str(self.get_top_unique_contribution()) + separator + \
               str(self.get_contribution_percent(self.get_top_unique_contribution()))


default_output_path = "./get_contrib_per_file_output/"
output_file = "highest_contributions.csv"

def main():
    unique_knowledge_file = sys.argv[1]

    output_path = default_output_path
    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    os.makedirs(output_path)

    with open(unique_knowledge_file, "r") as input:
        with open(os.path.join(output_path, output_file), "w") as output:
            output.write(KnowledgeFileData.highest_contribution_header)

            for line in input:
                knowledge_data = KnowledgeFileData(line)

                output.write(knowledge_data.to_highest_contribution_string(",") + "\n")
                # print(knowledge_data.to_highest_contribution_string(","))


if __name__ == "__main__":
    main()