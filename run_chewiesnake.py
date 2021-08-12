import os
import argparse
import pathlib
import json
import subprocess

CHEWIESNAKE_IMAGE_ID = os.getenv("CHEWIESNAKE_IMAGE_ID")
CHEWIESNAKE_MOUNT_POINT = os.getenv("CHEWIESNAKE_MOUNT_POINT")
BIFROST_DB_KEY = os.getenv("BIFROST_DB_KEY", "mongodb://localhost/bifrost_test")

parser = argparse.ArgumentParser(description='Run cheiwSnake with selected samples and save allele profiles to MongoDB.')
parser.add_argument('sample_names', help='Sample files to run on (strip read numbers and extension).')
args = parser.parse_args()

print(args.sample_names)