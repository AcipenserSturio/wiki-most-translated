import pandas as pd

df = pd.read_csv("csv/people-qid-metadata.tsv", sep="\t", header=None)
df = df.rename(columns={
    0: 'person',
    1: 'qid',
    2: 'birth',
    3: 'death',
    4: 'score',
    5: 'desc',
})
df = df[df["birth"] != "UNKNOWN"]
df = df[df["death"] != "UNKNOWN"]
# df = df[not (df["birth"] == "ALIVE" and df["birth"].astype(int) < 1900)]
# print(df)


df = (
    df
    # drop inconsistent rows
    .loc[~((df["death"] == "ALIVE") & (df["birth"].astype(int) < 1900))]

    # replace ALIVE with current year
    .assign(death=lambda x: x["death"].replace("ALIVE", "2026"))

    # cast to integers
    .assign(
        birth=lambda x: x["birth"].astype(int),
        death=lambda x: x["death"].astype(int),
        score=lambda x: x["score"].astype(int),
    )

    .assign(lifespan=lambda x: x["death"] - x["birth"])
)

df = df.loc[df["score"] >= 30]
df = df[df["birth"] >= -700]
df = df[df["birth"] < 2000]

df = (
    df
    .loc[df["lifespan"] < 120]
    .loc[df["lifespan"] > 4]

    # add decade column
    .assign(decade=lambda x: (x["birth"] // 10) * 10)

    # take top 10 per decade by score
    .sort_values(["decade", "score"], ascending=[True, False])
    .groupby("decade")
    .head(5)

    # optional: drop helper column
    .drop(columns="decade")
    .reset_index(drop=True)
)

df = df.sort_values(["death", "birth"], ascending=[True, True])

df = df.assign(cycle=lambda x: ((x["death"] - min(x["death"])) // 250) * 250)

df = df.assign(
    cycle_index=lambda x: x.groupby("cycle").cumcount()
)

df = df[
        ["person", "qid", "cycle_index", "birth", "death", "score", "desc"]
    ].rename(columns={
    'person': 'label',
    'qid': 'qid',
    'cycle_index': 'track',
    'birth': 'start',
    'death': 'end',
    'score': 'score',
    'desc': 'desc',
})

df.to_csv("csv/most-important.csv", index=False)
print(df)
