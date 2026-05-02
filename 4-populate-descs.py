
import requests
from tqdm import tqdm
import pandas as pd

WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"

headers = {
    'User-Agent': 'BotForMostTranslations/0.0 (https://kala-asi.li.pona.la/; kala.asi.la@gmail.com) bot-for-most-translations/0.0',
}

def fetch_desc(qid):

    url = WIKIDATA_API.format(qid)
    res = requests.get(url, headers=headers).json()
    entity = res["entities"].get(qid, {})


    desc = ""
    try:
        desc = entity["descriptions"]["en"]["value"]
    except Exception:
        pass
    print(qid, desc)
    return desc

# tqdm.pandas()
# df = pd.read_csv("temp/most-important.csv")
# df["desc"] = df["qid"].progress_apply(fetch_desc)
#
# df.to_csv("temp/most-important-with-descs.csv")



with open("temp/people-qid.tsv") as f:
    titles = f.read().split("\n")

with open("temp/qid-descs.tsv") as f:
    already_done = set(map(lambda x: x.split("\t")[0], f.read().split("\n")))

for title in tqdm(titles):
    person, qid = title.split("\t")
    if qid in already_done:
        continue

    desc = fetch_desc(qid)
    with open("temp/qid-descs.tsv", "a") as f:
        f.write("\t".join([qid, desc]) + "\n")
    already_done.add(qid)
