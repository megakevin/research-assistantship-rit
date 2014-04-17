#!/bin/bash

python3 get_sac_files_lines.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/sac-files-lines.csv
python3 get_contrib_distribution.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/contrib_distribution.csv
python3 get_line_count.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/line_count.csv
python3 get_comment_ratio.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/comment_ratio.csv
python3 get_defect_freq.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/defect_freq.csv
python3 get_complexity.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/complexity.csv
python3 get_satement_count.py /home/kevin/Desktop/sac-data/stats /home/kevin/Desktop/sac-data/statement_count.csv