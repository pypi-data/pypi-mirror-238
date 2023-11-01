# Quick Start

Most of the functionality is available via PyPi. If you only intend to use `ctxpro` for scoring and context extraction, you can install the lite version:

```
pip install ctxpro; pip install -U networkx
```

or to utilize the annotation capabilities:
```
pip install ctxpro[ext]; pip install -U networkx
```

Due to some unfortunate dependency issues, it is necessary to update `networkx` whenever installing `ctxpro`.
If you skip that step, you will get a `numpy` exception and instructions to upgrade `networkx`

There are three main functionalities of `ctxpro`

1. **Annotation** of new datasets

```
sacrebleu -t wmt22 -l en-de --echo docid src ref > wmt22.en-de.tsv
cat wmt22.en-de.tsv | ctxpro -r DE_GENDER DE_FORMALITY DE_AUXILIARY -t de
```

2. **Extraction** of document context from these annotations

```
cat annotations/*.json | jq -s add > wmt.en-de.json 
ctxpro-gen --input_files wmt22.en-de.tsv --annotations wmt.en-de.json > inputs.en-de.en
```

3. **Scoring* of translations

```
cat inputs.en-de.en | python scripts/deepl-translate.py de > translations.en-de.de
ctxpro-score -t translations.en-de.de -s wmt.en-de.json -l de
```

---

## Annotation

`ctxpro` reads from standard input or a list of files. The expected format is tab-delimited columns (docid, source, target).

### Rules

A series of predefined rules are provided as defined in the original paper. They are also located in the `data/rules` folder.
A predefined rule can be passed to `ctxpro` via the `--rule/-r` flag with the rule's name (`{DE,ES,FR,IT,PL,PT,RU}_{GENDER,AUXILIARY,FORMALITY}` or `{PL,RU}_INFLECTION`).

Alternatively, you can create your own. If you follow our structure, you can write a `.json` file (examples in `data/rules`) which the `ctxpro/checkers.py` classes will follow.

For the most flexibility, you can add your own system of criteria to the `ctxpro/checkers.py` file.

## Extraction

`ctxpro` can also be used to extract the preceding context from an annotated document set. The evaluations sets we release are based on OpenSubtitles. In order to extract context for your model, you must first download the data.

### Setting up OpenSubtitles

You have to setup OpenSubtitles for the language you care about. This includes downloading, unpacking, and then expanding into a format that organizes the files by year. Run the file `data/opensubtitles/setup.sh` to do this. It takes one argument, the language pair, e.g.,

    cd data/opensubs
    ./setup.sh de-en

### Extracting from an Evaluation Set

You can find our evaluation sets under `release`, but `ctxpro` will handle the downloading and processing. By default the data will be downloaded to `~/.ctxpro` but you can change this by setting the `CTXPRO` environment variable.

To print releases, you can call `ctxpro-list`. You can filter the output with the `--category/-c`, `--lang-pair/-l` and `--split/-s` flags.

## Benchmarking with existing test sets

This involves three steps:

1. Extract the sentences from the JSON file

   See the file release/json2tsv.sh, which iterates through all the files and creates
   the TSV files. It uses the script, ../scripts/json2tsv.py. Here is an example usage:

       cd release
       mkdir tsv
       ../scripts/json2tsv.py -s en -t de -d /path/to/opensubs --max-sents 10 --max-tokens 250 --separator " <eos>" --spm /path/to/spm --json-file auxiliary.opensubtitles.en-de.dev.json > /path/to/tsv/file

   This will create a TSV file using " <eos>" as a separator, and with up to 10 sentences or 250 tokens of context.

2. Translate the sentences with the decoder of your choice.

   The source field in the TSV is field 5 (1-indexed).

3. Score the outputs

   Use `scripts/score.py`. It takes the JSON file and the output, which are expected to be in order.

       cat output.txt | ./scripts/score.py --jsons /path/to/json/file --lang de

   The language is used for sentence splitting.


## Finding sentences in new documents

One version expects you to give input all the English files and it expects to find a parallel target language file (with the .en replaced) in the same directory. The script will print out a lot of debugging garbage, so you might want to pipe it somewhere. The script will write a separate output (.json) file for each `key` in the rules `.json` file.

If the `--cpu` is not passed and cuda is available, then I believe it will run coreference and word alignment on the gpu.

```
python search.py \
        --source_files opensubtitles/de-en/2017/*.en \
        --rules rules/de/de-all.json \
        --output_dir outputs/de/ \
        --target $tgt \
        --cpu
```

Alternatively, if no `--source_files` is passed, it will read from standard input expectecting a `docid`, `src`, `tgt` [tab-separated] column in that order.

```
sacrebleu -t wmt22 -l en-de --echo docid src ref | python search.py --rules rules/de/de-all.json --output_dir test-de --cpu
```

## Things I know need to be done

- [ ]  It should be possible to pass multiple `--rules` files (nargs)

- [ ] The Case, Gender, POS criteria should be actual regex matching instead of my string splicing logic

- [ ] Logical stdout/stderr prints

- [ ] Create a requirements.txt/environment yaml

- [ ] Batching for the processing so running on a gpu would be much more effective 

- [ ] download the spacy model if it does not exist rather than erroring out

## Python Environment

