# Welcome to the CORD-19-ANN Corpus

The CORD-19-ANN corpus is a collection of sentences extracted from research papers related to the novel coronavirus disease (COVID-19) detected in December 2019 in the province of Wuhan, China, which later expanded to nearly all the world. In reponse to the COVID-19 pandemic, an international alliance of doctors, scientists, researchers, and volunteers all over the world is leading an effort to understand, contain, and develop treatments for the SARS-CoV-2, the virus that causes the disease. As part of this effort, several academic publishers have made freely available thousands of research papers related to this and other coronavirus diseases.

This collection is extremely relevant since published research might contain clues to fight the epidemic hidden among thousands of different experimental reports, tables and figures, dicussion sections, etc. Manually digging through thousands of papers finding for these clues is unfeasible, so we must turn to artificial intelligence. However, it is very hard for algorithms to understand human language, even scientific, objective, language. We can ease this problem by providing the algorithms with a small set of sentences where humans manually annotate what's relevant and make explicit the semantic relations between different elements in the text.

Your mission, should you choose to accept it, is to manually annotate sentences extracted from these papers, a process in which you will select the most relevant elements mentioned and determine how they are semantically connected. As an example, let's take this sentence, shown here in its fully annotated glory.

![](docs/img1.png)

## Participate!

If you want to participate, [read the full instructions here](docs/instructions.md) and join our [Telegram group](https://t.me/cord19).
See a [demo video here](https://github.com/matcom/cord19-ann/raw/master/docs/demo.mp4).

## Contributors

This a list of everyone currently involved and what they are doing.

| **Pack** | **Side** | **Status**  | **Annotator**  | **Link** |
|----------|----------|-------------|----------------|----------|
|      1   | A        | Done        | @Estevanell    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack01/first/pack01-first) |
|      1   | B        | Done        | @nasobuco      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack01/second/pack01-second) |
|      2   | A        | Done        | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack02/first/pack02-first) |
|      2   | B        | In progress | @IntiBlanco    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack02/second/pack02-second) |
|      3   | A        | In progress | @Olivia        | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack03/first/pack03-first) |
|      3   | B        | Done        | @gabyfdez90    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack03/second/pack03-second) |
|      4   | A        | Done        | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack04/first/pack04-first) |
|      4   | B        | In progress | @TaniaMG       | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack04/second/pack04-second) |
|      5   | A        | Done        | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack05/first/pack05-first) |
|      5   | B        | In progress | @Dcardenas2019 | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack05/second/pack05-second) |
|      6   | A        | Done        | @DCardenas2019 | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack06/first/pack06-first) |
|      6   | B        | In progress | @Estevanell    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack06/second/pack06-second) |
|      7   | A        | Done        | @gabyfdez90    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack07/first/pack07-first) |
|      7   | B        | In progress | @AndyKIALO     | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack07/second/pack07-second) |
|      8   | A        | Done        | @gabyfdez90    | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack08/first/pack08-first) |
|      8   | B        | In progress | @Raffaaaaa     | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack08/second/pack08-second) |
|      9   | A        | In progress | @DrackEye      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack09/first/pack09-first) |
|      9   | B        | In progress | @DCardenas2019 | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack09/second/pack09-second) |
|     10   | A        | In progress | @DrackEye      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack10/first/pack10-first) |
|     10   | B        | In progress | @SusanitaLaDelRaton | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack10/second/pack10-second) |
|     11   | A        | Done        | @Skull_kiddf   | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack11/first/pack11-first) |
|     11   | B        | In progress | @luilver       | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack11/second/pack11-second) |
|     12   | A        | Done        | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack12/first/pack12-first) |
|     12   | B        | In progress | @k1ll3r99      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack12/second/pack12-second) |
|     13   | A        | Done        | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack13/first/pack13-first) |
|     13   | B        | Done        | @JOramas       | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack13/second/pack13-second) |
|     14   | A        | In progress | @danielvp      | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack14/first/pack14-first) |
|     14   | B        | In progress | @JOramas       | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack14/second/pack14-second) |
|     15   | A        | In progress | @Skull_kiddf   | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack15/first/pack15-first) |
|     15   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack15/second/pack15-second) |
|     16   | A        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack16/first/pack16-first) |
|     16   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack16/second/pack16-second) |
|     17   | A        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack17/first/pack17-first) |
|     17   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack17/second/pack17-second) |
|     18   | A        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack18/first/pack18-first) |
|     18   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack18/second/pack18-second) |
|     19   | A        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack19/first/pack19-first) |
|     19   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack19/second/pack19-second) |
|     20   | A        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack20/first/pack20-first) |
|     20   | B        |             |                | [🔗](http://ssh.apiad.net:8080/#/cord19/packs/pack20/second/pack20-second) |
