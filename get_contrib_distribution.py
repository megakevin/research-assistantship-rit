# Usage: $ python3 merge_contrib_distribution.py /home/kevin/Desktop/sac-data/stats
#          python3 merge_contrib_distribution.py <merged_files>
#
# Merges all the extracted contribution per tag data into one single file.

__author__ = 'kevin'

import sys
import csv
import os

contrib_file_prefix = "contrib_"
contrib_file_extension = ".csv"
single_authored_threshold = 90.0

# RQ 1: Generate a csv file for each project with: file, release, if its SAC, LOC
csv_header = ['project', '0%', '5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%',
              '55%','60%', '65%', '70%', '75%', '80%', '85%', '90%', '95%', '100%']

def main(argv):

    data_dir = argv[1]
    output_file = argv[2]

    result = []

    contribution = 'top_single_dev_contribution_knowledge_percent'

    for data_file in os.listdir(data_dir):
        with open(os.path.join(data_dir, data_file), newline="") as csv_file:
            data = [float(row[contribution]) for row in csv.DictReader(csv_file)]

        result.append({
            'project': data_file,
            '0%': len([c for c in data if (0 <= c < 5)]),
            '5%': len([c for c in data if (5 <= c < 10)]),
            '10%': len([c for c in data if (10 <= c < 15)]),
            '15%': len([c for c in data if (15 <= c < 20)]),
            '20%': len([c for c in data if (20 <= c < 25)]),
            '25%': len([c for c in data if (25 <= c < 30)]),
            '30%': len([c for c in data if (30 <= c < 35)]),
            '35%': len([c for c in data if (35 <= c < 40)]),
            '40%': len([c for c in data if (40 <= c < 45)]),
            '45%': len([c for c in data if (45 <= c < 50)]),
            '50%': len([c for c in data if (50 <= c < 55)]),
            '55%': len([c for c in data if (55 <= c < 66)]),
            '60%': len([c for c in data if (60 <= c < 65)]),
            '65%': len([c for c in data if (65 <= c < 70)]),
            '70%': len([c for c in data if (70 <= c < 75)]),
            '75%': len([c for c in data if (75 <= c < 80)]),
            '80%': len([c for c in data if (80 <= c < 85)]),
            '85%': len([c for c in data if (85 <= c < 90)]),
            '90%': len([c for c in data if (90 <= c < 95)]),
            '95%': len([c for c in data if (95 <= c < 100)]),
            '100%': len([c for c in data if (c >= 100)]),
        })

    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, csv_header)
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    main(sys.argv)
