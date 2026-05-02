import requests
from tqdm import tqdm
import pandas as pd

WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"

# Edge case constants
UNKNOWN = "UNKNOWN"
ALIVE = "ALIVE"
headers = {
    'User-Agent': 'BotForMostTranslations/0.0 (https://kala-asi.li.pona.la/; kala.asi.la@gmail.com) bot-for-most-translations/0.0',
}

def extract_year(date_str):
    # print(date_str)
    # Format example: "+1958-08-29T00:00:00Z"
    if not date_str:
        return UNKNOWN
    return int(date_str[:5].replace("+", ""))

def get_metadata(wikidata_id):
    if not wikidata_id:
        return UNKNOWN, UNKNOWN, "0"

    url = WIKIDATA_API.format(wikidata_id)
    res = requests.get(url, headers=headers).json()

    # print(res)

    entity = res["entities"].get(wikidata_id, {})
    claims = entity.get("claims", {})

    # Birth
    birth = UNKNOWN
    if "P569" in claims:
        try:
            birth = extract_year(
                claims["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            )
        except Exception:
            pass

    # Death
    death = ALIVE
    if "P570" in claims:
        try:
            death = extract_year(
                claims["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
            )
        except Exception:
            death = UNKNOWN

    # Score
    score = len(list(filter(lambda x: x[-4:] == "wiki", entity.get("sitelinks", {}).keys())))

    # Desc
    desc = ""
    try:
        desc = entity["descriptions"]["en"]["value"]
    except Exception:
        pass

    return str(birth), str(death), str(score), desc


with open("csv/people-qid.tsv") as f:
    titles = f.read().split("\n")

with open("csv/people-qid-metadata.tsv") as f:
    already_done = set(map(lambda x: x.split("\t")[0], f.read().split("\n")))

for title in tqdm(titles):
    person, qid = title.split("\t")
    if person in already_done:
        continue

    print(title)
    birth, death, score, desc = get_metadata(qid)
    with open("csv/people-qid-metadata.tsv", "a") as f:
        f.write("\t".join([person, qid, birth, death, score, desc]) + "\n")
    already_done.add(person)
