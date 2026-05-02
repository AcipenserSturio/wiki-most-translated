import requests
from tqdm import tqdm
import pandas as pd

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# Edge case constants
headers = {
    'User-Agent': 'BotForMostTranslations/0.0 (https://kala-asi.li.pona.la/; kala.asi.la@gmail.com) bot-for-most-translations/0.0',
}

def get_wikidata_id(title):
    params = {
        "action": "query",
        "prop": "pageprops",
        "titles": title,
        "format": "json"
    }
    res = requests.get(
        WIKIPEDIA_API,
        headers=headers,
        params=params,
    )
    # print(res.content)
    if res.content[0] != 123:
        raise Exception(res.content[0])
    res = res.json()
    pages = res["query"]["pages"]

    for page in pages.values():
        return page.get("pageprops", {}).get("wikibase_item")

    return None


with open("temp/people-lvl-5.txt") as f:
    titles = f.read().split("\n")

with open("temp/people-lvl-4.txt") as f:
    titles += f.read().split("\n")

with open("temp/people-lvl-3.txt") as f:
    titles += f.read().split("\n")

with open("temp/people-100-translations.txt") as f:
    titles += f.read().split("\n")

with open("temp/people-qid.tsv") as f:
    already_done = set(map(lambda x: x.split("\t")[0], f.read().split("\n")))

for title in tqdm(titles):
    if title in already_done:
        continue

    qid = get_wikidata_id(title)
    with open("temp/people-qid.tsv", "a") as f:
        f.write(f"{title}\t{qid}\n")
    already_done.add(title)
