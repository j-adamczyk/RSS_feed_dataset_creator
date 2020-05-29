import csv
import feedparser
import html2text
import json
import re


if __name__ == "__main__":
    with open("sites.json") as json_file:
        data = json.load(json_file)

        with open("out.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([["label", "text"]])

        for document in data:
            label = document["label"]
            urls = document["urls"]

            results = []
            for url in urls:
                response = feedparser.parse(url)
                html_to_text = html2text.HTML2Text()
                html_to_text.ignore_emphasis = True
                html_to_text.ignore_images = True
                html_to_text.ignore_links = True
                html_to_text.ignore_tables = True

                url_results = []
                for item in response.entries:
                    try:
                        title = item.title
                        if title[-1] not in {".", "?", "!"}:
                            title = title + "."

                        text = title + " " + html_to_text.handle(item.description)
                        text = re.sub(r"\*|\[...\]|\\-$", "", text)
                        text = re.sub(r"http\S+", "", text)
                        text = re.sub(r"\s+", " ", text)
                        results.append([label, text])
                    except:
                        pass

            with open("out.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerows(results)
