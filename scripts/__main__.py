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
            entities.add((keyphrase.text, keyphrase.label))

    for e in sorted(entities):
        print("\t".join(e))


def extract_corpus_relations():
    corpus = load_training_data("cord19")

    relations = set()

    for sentence in corpus.sentences:
        for relation in sentence.relations:
            relations.add((relation.from_phrase.text, relation.label, relation.to_phrase.text))

    for e in sorted(relations):
        print("\t".join(e))



if __name__ == "__main__":
    fire.Fire()
