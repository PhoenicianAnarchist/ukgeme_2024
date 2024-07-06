#!/usr/bin/env python3
import pathlib
import requests
import lxml.etree
import json

def get_cached(url, filepath, force_refresh=False):
    if filepath.is_file() and (not force_refresh):
        return filepath

    r = requests.get(url)

    dir = filepath.parent
    if (not dir.exists()):
        dir.mkdir(parents=True)

    with open(filepath, "wb") as f:
        f.write(r.content)

    return filepath

def get_constituency_data(name, url, filepath):
    filepath = get_cached(url, filepath)
    tree = lxml.etree.parse(filepath, lxml.etree.HTMLParser())

    json_data = {}
    json_data["meta"] = {}
    json_data["meta"]["name"] = name
    json_data["meta"]["registered"] = int(
        tree.xpath(
            '//div[@class="ssrcss-1p1ocz-TextField enm63mj2"]/span[2]'
        )[0].text.replace(",", "")
    )

    total_votes = 0
    json_data["scorecards"] = []
    for scorecard in tree.xpath('//div[@data-testid="scorecard-proper"]'):
        scorecard_data = get_scorecard_data(scorecard)
        json_data["scorecards"].append(scorecard_data)
        total_votes += scorecard_data["vote_count"]

    json_data["meta"]["vote_count"] = total_votes
    json_data["meta"]["turnout"] = total_votes / json_data["meta"]["registered"]
    return json_data

def get_scorecard_data(scorecard):
    json_data = {}

    json_data["party"] = scorecard.xpath(
        '*//*[@class="ssrcss-qqwz3f-Supertitle e1j83d2f3"]'
    )[0].text

    json_data["candidate"] = scorecard.xpath(
        '*//*[@class="ssrcss-h5cxh6-Title e1j83d2f2"]'
    )[0].text

    json_data["vote_count"] = int(
        scorecard.xpath(
            '*//*[@class="ssrcss-a2di88-ResultValue e1k9l0jz0"]'
        )[0].text.replace(",", "")
    )

    return json_data

if __name__ == "__main__":
    domain = "https://www.bbc.co.uk/"
    url = f"{domain}/news/election/2024/uk/constituencies"
    web_cache_path = pathlib.Path("./cache/bbc2024.html")
    json_data_path = pathlib.Path("./data/bbc2024.json")

    web_cache_path = get_cached(url, web_cache_path)
    tree = lxml.etree.parse(web_cache_path, lxml.etree.HTMLParser())

    elements = tree.xpath('//div[@class="ssrcss-u3oqoy-Callout ewuptu24"]')

    json_data = {}
    for element in elements:
        path = pathlib.Path(element.xpath('a')[0].attrib["href"])
        constituency_id = path.name

        constituency_cache_path = pathlib.Path(
            f"./cache/constituencies/{constituency_id}.html"
        )

        name = element.xpath('a')[0].text
        print(f"Fetching data for : {constituency_id} {name}")
        url = f"{domain}{path}"
        json_data[name] = get_constituency_data(
            name, url, constituency_cache_path
        )

    json_data_dir = json_data_path.parent
    if (not json_data_dir.exists()):
        json_data_dir.mkdir(parents=True)

    with open(json_data_path, "w") as f:
        json.dump(json_data, f, indent=2, sort_keys=True)
