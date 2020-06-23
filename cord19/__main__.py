import logging
import collections
import json
import numpy as np
import fire
import pandas as pd
import altair as alt
import tqdm
import networkx as nx

from pathlib import Path

from sklearn.model_selection import train_test_split
from .classifier import Model
from .data import load_corpus, load_training_data
from .utils import Collection
from .score import full_evaluation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cord19.cli")


def train_test(
    negative_sampling: float = 0.25, train_size: float = 0.8, iterations: int = 30
):
    corpus = load_training_data("cord19")

    metrics = []

    with open("data/output/evaluation.jsonl", "w") as fp:
        for i in range(iterations):
            logger.info("Iteration=%i" % i)
            train, test = train_test_split(corpus, train_size=train_size)

            model = Model(train, negative_sampling=negative_sampling)
            model.train()

            gold = Collection(test)

            for threshold in np.arange(start=0.0, stop=3.0, step=0.25):
                model.max_entity_uncertainty = threshold
                model.max_relation_uncertainty = threshold
                predicted = model.predict(test)

                m = compute_score(gold, predicted)
                m["threshold"] = threshold
                metrics.append(m)
                fp.write(json.dumps(m) + "\n")
                print(m)


def extract_corpus_entities():
    corpus = load_training_data("cord19")

    entities = set()

    for sentence in corpus.sentences:
        for keyphrase in sentence.keyphrases:
            entities.add((keyphrase.text, keyphrase.label))

    for e in sorted(entities):
        print("\t".join(e))


def extract_corpus_relations():
    corpus = load_training_data("cord19")

    relations = set()

    for sentence in corpus.sentences:
        for relation in sentence.relations:
            relations.add(
                (relation.from_phrase.text, relation.label, relation.to_phrase.text)
            )

    for e in sorted(relations):
        print("\t".join(e))


def compute_agreement():
    corpus = load_training_data("cord19")
    sentences = sorted(corpus, key=lambda s: s.text)

    collection1 = Collection([s for i, s in enumerate(sentences) if i % 2 == 0])
    collection2 = Collection([s for i, s in enumerate(sentences) if i % 2 != 0])

    return compute_score(collection1, collection2)


def compute_score(gold: Collection, pred: Collection):
    score = dict(full=full_evaluation(gold, pred))

    # agreement for entities
    for l in [
        "Action",
        "Concept",
        "Reference",
    ]:
        c1 = gold.clone(keep_labels=[l])
        c2 = pred.clone(keep_labels=[l])

        score[l] = full_evaluation(c1, c2)

    # agreement for entities
    for l in [
        "is-a",
        "in-place",
        "in-time",
        "in-context",
        "subject",
        "target",
        "has-property",
        "has-part",
        "causes",
        "entails",
    ]:
        c1 = gold.clone(keep_labels=["Concept", "Action", "Reference", l])
        c2 = pred.clone(keep_labels=["Concept", "Action", "Reference", l])

        score[l] = full_evaluation(c1, c2)

    return score


def compute_statistics(collection: int = 0):
    corpus = load_training_data("cord19")
    sentences = sorted(corpus, key=lambda s: s.text)

    collection1 = Collection([s for i, s in enumerate(sentences) if i % 2 == 0])
    collection2 = Collection([s for i, s in enumerate(sentences) if i % 2 != 0])

    corpora = [corpus, collection1, collection2]
    corpus = corpora[collection]

    stats = collections.Counter(Sentences=len(corpus))

    for s in corpus.sentences:
        for k in s.keyphrases:
            stats[k.label] += 1
    stats["Entities"] = sum(stats[e] for e in ["Action", "Concept", "Reference"])

    for s in corpus.sentences:
        for r in s.relations:
            stats[r.label] += 1
    stats["Relations"] = sum(stats[e] for e in stats if e.islower())

    for s in corpus.sentences:
        for k in s.keyphrases:
            for a in k.attributes:
                stats[a.label] += 1
    stats["Attributes"] = sum(
        stats[e] for e in ["Negated", "Diminished", "Emphasized", "Uncertain"]
    )

    return stats


def training_results():
    data = []

    with open("data/output/evaluation.jsonl") as fp:
        for line in fp:
            datum = json.loads(line)
            th = datum.pop("threshold")
            for key, value in datum.items():
                value["key"] = key
                value["threshold"] = th
                data.append(value)

    df = pd.DataFrame(data)

    full = df[df["key"] == "full"].groupby("threshold").mean().round(3)
    print(full.to_latex())

    rest_e = (
        df[df["key"].isin(["Action", "Concept", "Reference"])]
        .groupby(["threshold", "key"])
        .mean()
        .round(3)
    )
    rest_e = rest_e.reset_index().copy()
    rest_e["precision"] = rest_e["entity_precision"]
    rest_e["recall"] = rest_e["entity_recall"]
    rest_e["f1"] = rest_e["entity_f1"]

    rest_r = (
        df[
            df["key"].isin(
                [
                    "is-a",
                    "in-place",
                    "in-time",
                    "in-context",
                    "subject",
                    "target",
                    "has-property",
                    "has-part",
                    "causes",
                    "entails",
                ]
            )
        ]
        .groupby(["threshold", "key"])
        .mean()
        .round(3)
    )
    rest_r = rest_r.reset_index().copy()
    rest_r["precision"] = rest_r["relation_precision"]
    rest_r["recall"] = rest_r["relation_recall"]
    rest_r["f1"] = rest_r["relation_f1"]

    rest = pd.concat([rest_e, rest_r])

    chart = (
        alt.Chart(rest[rest["recall"] > 0.1])
        .mark_line()
        .encode(
            x=alt.X("threshold", title="Threshold"),
            y=alt.Y("precision", title="Precision @ Recall > 0.1"),
            color=alt.Color("key", title="Element"),
        )
        .properties(width=400, height=300)
    )

    chart.save("data/output/fitness.html")

    rest = rest[["precision", "recall", "f1", "key"]]
    print(rest.groupby("key").max().to_latex())


def execute_model(negative_sampling: float = 0.25, batch_size: int = 100):
    corpus = load_training_data("cord19")
    model = Model(corpus, negative_sampling=negative_sampling)
    model.train()

    sentences = []

    with open("data/cord19/corpus/raw.txt") as fp:
        for line in fp:
            sentences.append(line.strip())

    batch = []
    batch_n = 1

    for s in tqdm.tqdm(sentences):
        batch.append(s)

        if len(batch) >= batch_size:
            collection = model.predict(batch)
            collection.dump(Path(f"data/output/predicted/batch_{batch_n}.txt"))

            with open(f"data/output/predicted/batch_{batch_n}.scores", "w") as fp:
                for s in collection:
                    for key in s.keyphrases:
                        fp.write(f"T{key.id}:{key.uncertainty:.4f}\n")
                    for rel in s.relations:
                        fp.write(f"R{rel.id}:{rel.uncertainty:.4f}\n")

            batch_n += 1
            batch = []


def predicted_stats(max_files=None):
    corpus = load_training_data("output", max_files)

    counter_entities = collections.Counter()
    counter_relations = collections.Counter()
    counter_labels = collections.Counter()

    def blacklist(e):
        if e.lower() in [
            "cc",
            "-",
            "%",
            "license",
            "by",
            "international",
            "medrxiv",
            "preprint",
            "rights",
            "reserved",
            "non",
        ]:
            return True

        if e[0].isdigit():
            return True

        if len(e) < 3:
            return True

        return False

    graph = nx.DiGraph()

    for s in corpus:
        counter_labels["Sentence"] += 1

        for k in s.keyphrases:
            if blacklist(k.text):
                continue

            counter_labels["Entities"] += 1
            counter_labels[k.label] += 1

            if k.label == "Concept":
                counter_entities[k.text] += 1

        for r in s.relations:
            if blacklist(r.from_phrase.text) or blacklist(r.to_phrase.text):
                continue

            counter_relations[(r.from_phrase.text, r.label, r.to_phrase.text)] += 1
            counter_labels["Relations"] += 1
            counter_labels[r.label] += 1

    print(
        pd.DataFrame(counter_labels.items(), columns=["Type", "Instances"])
        .set_index("Type")
        .to_latex()
    )

    print(
        pd.DataFrame(counter_entities.most_common(20), columns=["Concept", "Instances"])
        .set_index("Concept")
        .to_latex()
    )

    df = pd.DataFrame(
        [
            dict(Source=e1, Destination=e2, Relation=r, Count=c)
            for (e1, r, e2), c in counter_relations.items()
            if e1 != e2
        ]
    ).sort_values("Count", ascending=False)

    best_is_a = df[df['Relation'] == 'is-a'].head(5)
    best_has_p = df[df['Relation'] == 'has-property'].head(5)

    best = pd.concat([best_is_a, best_has_p])
    print(best.set_index('Relation').to_latex())


if __name__ == "__main__":
    fire.Fire()
