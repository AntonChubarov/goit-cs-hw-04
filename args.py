import argparse

parser = argparse.ArgumentParser(description="search for a keyword in files")
parser.add_argument("directory", help="directory to search")
parser.add_argument("keyword", help="keyword to search")
args = parser.parse_args()
