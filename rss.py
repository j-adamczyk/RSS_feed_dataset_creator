import csv
import json
import re

import feedparser
import html2text


def parse(url, label, create=False, output_file=None):
    if create and not output_file:
        raise ValueError("If create=True, then output_file has to be provided")

    if create:
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([["labels", "text"]])

    response = feedparser.parse(url)
    html_to_text = html2text.HTML2Text()
    html_to_text.ignore_emphasis = True
    html_to_text.ignore_images = True
    html_to_text.ignore_links = True
    html_to_text.ignore_tables = True

    results = []
    for item in response.entries:
        try:
            title = item.title
            if title and title[-1] not in {".", "?", "!"}:
                title = title + "."

            text = title + " " + html_to_text.handle(item.description)
            text = re.sub(r"\*|\[...\]|\\-$", "", text)
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r"\s+", " ", text)
            results.append([label, text])
        except:
            pass

    if output_file:
        with open(output_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(results)

    return results


class RSSParser:
    def __init__(self, file=None):
        self.file = file

    def parse(self, data=None, create=False, output_file=None):
        if not self.file and not data:
            raise ValueError("Either set 'file' attribute or pass 'data' argument in an appropriate format")

        if create and not output_file:
            raise ValueError("If create=True, then output_file has to be provided")

        if not data and self.file:
            with open(self.file) as file:
                data = json.load(file)

        if len(data) == 0:
            return []

        if create:
            with open(output_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows([["labels", "text"]])

        all_results = []
        for document in data:
            label = document["label"]
            urls = document["urls"]

            single_document_results = []
            for url in urls:
                single_url_results = parse(url, label)
                single_document_results.extend(single_url_results)

            all_results.extend(single_document_results)

            if output_file:
                with open(output_file, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writerows(single_document_results)

        return all_results
