################################ PACKAGING AND LOGGING ################################
import pathlib
import logging
import os, sys
from typing import List, Set, Dict, Tuple

if (__package__ is None or __package__ == "") and __name__ == '__main__':
    parent = pathlib.Path(__file__).absolute().parents[1]
    sys.path.insert(0, str(parent))
    __package__ = 'ctxpro'


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    stream=sys.stderr,
)
logger = logging.getLogger("ctxpro")


################################ IMPORTS ################################

import argparse
import tqdm

from .datasets import get_test_data


################################ FUNCTIONALITY ################################

def get_ostream(output):
    """
    Handles the output stream.
    """
    if output is None:
        return sys.stdout
    else:
        return open(output, 'r')


def get_documents(istream):
    documents = {}
    logger.info("Reading input...")
    for docid, src, tgt in tqdm.tqdm(read_input(istream)):
        if docid not in documents:
            documents[docid] = []
        documents[docid].append(src)
    return documents 

def read_input(input_stream):
    """
        Returns a single line at a time to the document generator.
        Will either return lines from standard input, or iterate over the files in a list
        If input_files is None, stdin is read. Otherwise, a tsv file is expected.
        Format should be tab-delimited columns of document, source, target.
    """
    if input_stream is None:
        logger.debug("Reading from stdin...")
        for line in sys.stdin:
            if len(line.strip().split("\t")) != 3:
                raise Exception("Input must be tab-delimited columns of document, source, target.")
            docid, src, tgt = line.strip().split("\t")
            yield docid, src, tgt
    else:
        logger.debug("Reading from input files...")
        for fi in input_stream:
            with open(fi) as infile:
                for line in infile:
                    if len(line.strip().split("\t")) != 3:
                        raise Exception("Input must be tab-delimited columns of document, source, target.")
                    docid, src, tgt = line.strip().split("\t")
                    yield docid, src, tgt


def count_tokens(line, spm):
    return len(spm.encode(line) if spm else line.split())


def get_context(documents, docid, segment_id, max_tokens, max_sentences, spm=None):
    """
    For a specific annotated example, iterates over the original data and extracts the context
    An SPM model is used if passed
    This will be slow on very large inputs
    """
    context_start = max(segment_id - max_sentences, 0)
    context_lines = documents[docid][context_start:segment_id]

    length = sum([count_tokens(_, spm) + 1 for _ in context_lines])
    while length > max_tokens:
        s = context_lines.pop(0)
        length -= count_tokens(s, spm) - 1
    return context_lines


def extract(args):
    """
    Extracts the context for each annotated example.
    Adjoins them with a connecting string.
    """
    spm = None
    if args.spm is not None:
        import sentencepiece as sp
        spm = sp.SentencePieceProcessor(model_file=args.spm)

    annotation = get_test_data(args.annotations)
    ostream = get_ostream(args.output)
    documents = get_documents(args.input_files)

    for example in annotation:

        document_id = example["document id"]
        segment_id = example["segment id"]

        contexts = get_context(documents, document_id, segment_id, args.max_tokens, args.max_sentences, spm)

        print(args.adjoining_string.join(contexts), file=ostream)


def parse_args():
    parser = argparse.ArgumentParser(
        description="CTXPRO: Extract machine translation source-side inputs with preceding context.\n"
        "   Example: ctxpro-gen -i wmt22.en-de.tsv -s wmt_extracted.json",
        usage="$(prog)s [-H] [-i INPUT_FILES] [-r RULES] -t [TARGET] -o [OUTPUT_DIR] [OPTIONS]",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--input_files", '-i', default=None,
                                                type=str,
                                                nargs='*',
                                                help = "Input tsv files that have already been annotated. Expected columns are docid, src, tgt.")
    parser.add_argument("--annotations", '-a', default=None,
                                                type=str,
                                                help = "Input tsv files that have already been annotated. If not specified, reads from stdin. Expected columns are docid, src, tgt.")
    parser.add_argument("--max_sentences", '-s', default=10,
                                                type=int,
                                                help="The maximum number of sentences to include.")
    parser.add_argument("--max_tokens", "-t", default=10000,
                                                type=int,
                                                help="The maximum number of tokens to include.")
    parser.add_argument("--spm", "-S", default=None,
                                                type=str,
                                                help="Path to sentencepiece model. If not specified, uses whitespace tokenization.")
    parser.add_argument("--adjoining_string", default=" ",
                                                type=str,
                                                help="The string to use to join sentences together. Defaults to a space.")
    parser.add_argument("--output", "-o", default=None,
                                            type=str,
                                            help="The output file to write to. If not specified, writes to stdout.")
    parser.add_argument("--version", '-v', default=False, action="store_true", help="Prints version and exits.")

    args = parser.parse_args()

    return args


def main():


    args = parse_args()

    if args.version:
        from . import __version__
        print(f"CTXPRO version {__version__}")
        sys.exit(0)


    extract(args)
                             
if __name__ == "__main__":
    main()