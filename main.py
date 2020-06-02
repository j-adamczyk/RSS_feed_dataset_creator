import csv
import json


from rss import RSSParser


if __name__ == "__main__":
    parser = RSSParser(file="sites.json")
    parser.parse(output_file="out.csv", create=True)
