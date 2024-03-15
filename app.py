import argparse
import os
parser = argparse.ArgumentParser(description="Download video from psitoffers.store")
parser.add_argument('csv_file', help="list of csv_files")
args = parser.parse_args()

file = args.csv_file
if os.path.exists(file):
    print("File exists: Continuing ")
