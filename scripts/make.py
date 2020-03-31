import fire
import os
import yaml
from pathlib import Path


def report():
    with open(Path(__file__).parent / "packs.yml") as fp:
        packs = yaml.safe_load(fp)['packs']

    result = []

    with open(Path(__file__).parent.parent / "README.md") as fp:
        for line in fp:
            result.append(line.strip("\n"))

            if line.startswith("## Contributors"):
                break

    result.append("""
This a list of everyone currently involved and what they are doing.

| **Pack** | **Side** | **Status**     | **Annotator**        | **Link** |
|----------|----------|----------------|----------------------|----------|""")

    for pack_id, pack in packs.items():
        for label, (version_id, version) in zip("AB", pack.items()):
            result.append(f"| {pack_id[4:]:8} | {version_id:8} | {version['status']:14} | {version['assigned'] or '':20} | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/{pack_id}/{version_id}/{pack_id}-{version_id}) |")

    with open(Path(__file__).parent.parent / "README.md", "w") as fp:
        for line in result:
            fp.write(line + "\n")


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

        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}", 0o777)
        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version, 0o777)
        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.txt", 0o777)
        os.chmod(Path(__file__).absolute().parent.parent / "data" / "cord19" / "packs" / f"pack{number}" / version / f"pack{number}-{version}.ann", 0o777)

    for sentence in sentences:
        print(sentence)


if __name__ == "__main__":
    fire.Fire()