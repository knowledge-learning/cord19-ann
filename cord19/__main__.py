import logging

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

    for i in range(iterations):
        logger.info("Iteration=%i" % i)
        train, test = train_test_split(corpus, train_size=train_size)

        model = Model(train, negative_sampling=negative_sampling)
        model.train()

        predicted = model.predict(test[:10])
        gold = Collection(test[:10])

        metrics.append(full_evaluation(gold, predicted))

    print(pd.DataFrame(metrics).describe().to_markdown())


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


if __name__ == "__main__":
    fire.Fire()
