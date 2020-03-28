import fire
import os

from pathlib import Path


def pack(number: str):
    sentences = []

    with open(Path(__file__).absolute().parent.parent / "data" / "cord19" / "corpus" / "raw.txt") as fp:
        for sentence in fp:
            if len(sentences) == 5:
                break

            sentence = sentence.strip()
            
            if not sentence:
                raise ValueError("Empty sentence before finishing")

            sentences.append(sentence)

    for version in ["first", "second"]:
        os.makedirs(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version, exist_ok=True)
        
        with open(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.txt", "w") as fp:
            for sentence in sentences:
                fp.write(sentence)
                fp.write("\n")

        with open(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.ann", "w") as fp:
            pass

        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.txt", 0o777)
        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.ann", 0o777)

    for sentence in sentences:
        print(sentence)


if __name__ == "__main__":
    fire.Fire()