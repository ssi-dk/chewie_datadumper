import os
import argparse
import pathlib
import subprocess

CHEWIESNAKE_IMAGE_ID = os.getenv("CHEWIESNAKE_IMAGE_ID")
CHEWIESNAKE_MOUNT_POINT = os.getenv("CHEWIESNAKE_MOUNT_POINT")
BIFROST_DB_KEY = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")

parser = argparse.ArgumentParser(description='Run chewieSnake with selected samples and save allele profiles to MongoDB.')
parser.add_argument('-s','--sample_names', nargs='+', help='Sample names (strip read numbers and extension from file names).')
args = parser.parse_args()

lines = ["sample\tfq1\tfq2\n"]

for sample_name in args.sample_names:
    file_name_1 = f"{sample_name}_R1_001.fastq.gz"
    file_name_2 = f"{sample_name}_R2_001.fastq.gz"
    line = f"{sample_name}\t/chewieSnake/analysis/{file_name_1}\t/chewieSnake/analysis/{file_name_2}"
    lines.append(line)

mount_point = pathlib.Path(CHEWIESNAKE_MOUNT_POINT)
assert mount_point.exists()
samples_tsv_path = pathlib.Path(mount_point, 'samples.tsv')

with open(samples_tsv_path, 'w') as file:
    file.writelines(lines)
    file.write("\n")

command = f"""docker run --rm \
-v {CHEWIESNAKE_MOUNT_POINT}:/chewieSnake/analysis \
-e LOCAL_USER_ID=$(id -u $USER) \
{CHEWIESNAKE_IMAGE_ID} \
--reads \
--sample_list /chewieSnake/analysis/samples.tsv \
--scheme /chewieSnake/analysis/enterobase_senterica_cgmlst \
--prodigal /chewieSnake/analysis/Salmonella_enterica.trn \
--working_directory /chewieSnake/analysis/output
"""
print("Command:")
print(command)