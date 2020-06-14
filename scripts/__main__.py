import logging

import fire

from .classifier import Model
from .data import load_corpus, load_training_data

logging.basicConfig(level=logging.INFO)


def train(negative_sampling: float = 0.25):
    corpus = load_training_data("cord19")
    model = Model(corpus, negative_sampling=negative_sampling)
    model.train()


def extract_corpus_entities():
    corpus = load_training_data("cord19")

    entities = set()

    for sentence in corpus.sentences:
        for keyphrase in sentence.keyphrases:
            entities.add(keyphrase.text)

    for e in sorted(entities):
        print(e)


if __name__ == "__main__":
    fire.Fire()
