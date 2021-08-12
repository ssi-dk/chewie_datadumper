import os
import argparse
import pathlib
import json
import subprocess

CHEWIESNAKE_IMAGE_ID = os.getenv("CHEWIESNAKE_IMAGE_ID")
CHEWIESNAKE_MOUNT_POINT = os.getenv("CHEWIESNAKE_MOUNT_POINT")
BIFROST_DB_KEY = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")

parser = argparse.ArgumentParser(description='Run cheiwSnake with selected samples and save allele profiles to MongoDB.')
parser.add_argument('-s','--sample_names', nargs='+', help='Sample names (strip read numbers and extension from file names).')
args = parser.parse_args()

lines = ["sample\tfq1\tfq2"]

for sample_name in args.sample_names:
    file_name_1 = f"{sample_name}_R1_001.fastq.gz"
    file_name_2 = f"{sample_name}_R2_001.fastq.gz"
    line = f"{sample_name}\t/chewieSnake/analysis/{file_name_1}\t{file_name_2}"
    lines.append(line)

with open('samples.tsv', 'w') as file:
    file.writelines(lines)