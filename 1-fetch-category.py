import requests

API_URL = "https://en.wikipedia.org/w/api.php"

headers = {
    'User-Agent': 'BotForMostTranslations/0.0 (https://kala-asi.li.pona.la/; kala.asi.la@gmail.com) bot-for-most-translations/0.0',
}

# CATEGORY = "Category:Wikipedia_level-5_vital_articles_in_People"
CATEGORY = "Category:Wikipedia_level-4_vital_articles_in_People"
# CATEGORY = "Category:Wikipedia_level-3_vital_articles_in_People"

def fetch_category_members(cmcontinue=None):
    params = {
        "action": "query",
        "format": "json",
        "generator": "categorymembers",
        "gcmtitle": CATEGORY,
        "gcmlimit": "500"
    }

    if cmcontinue:
        params["gcmcontinue"] = cmcontinue

    res = requests.get(API_URL, params=params, headers=headers).json()

    pages = res.get("query", {}).get("pages", {})

    results = []
    for page_id, page in pages.items():
        results.append(page["title"].replace("Talk:", ""))

    continue_token = res.get("continue", {}).get("gcmcontinue")

    return results, continue_token


all_results = []
cont = None

while True:
    batch, cont = fetch_category_members(cont)
    all_results.extend(batch)

    if not cont:
        break

print(f"Fetched {len(all_results)} entries")

with open("temp/people-lvl-4.txt", "w") as f:
    f.write("\n".join(all_results))
