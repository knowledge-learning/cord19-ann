import logging
import collections
import json
import numpy as np
import fire
import pandas as pd

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

    with open("data/output/evaluations.jsonl") as fp:   
        for line in fp:
            data.append(json.loads(line))

    return data


if __name__ == "__main__":
    fire.Fire()
