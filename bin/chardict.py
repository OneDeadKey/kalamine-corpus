#!/usr/bin/env python3
"""Turn corpus texts into dictionaries of n-grams."""

import json
from pathlib import Path
from sys import argv

NGRAM_MAX_LENGTH = 4  # trigrams
IGNORED_CHARS = "1234567890 \t\r\n\ufeff↵"


def parse_corpus(txt: str) -> dict:
    """Count ngrams in a string.
    retuns a dict of ngrams
        ngrams[1]=symbols
        ngrams[2]=bigrames
        ngrams[3]=trigrams
        etc., up to NGRAM_MAX_LENGTH
    ngrams[2] is shaped as { "aa": count }
    """

    ngrams = {}
    ngrams_count = {}  # ngrams_count counts the total number of ngrams[i] in corpus.

    txt = txt.lower()  # we want to be case **in**sensitive

    for ngram in range(1, NGRAM_MAX_LENGTH):
        ngrams[ngram] = {}
        ngrams_count[ngram] = 0

    def get_ngram(txt: str, ngram_start: int, ngram_length: int) -> str:
        """get a ngram of a given length at given position in txt
        returns empty string if ngram cannot be provided"""
        if txt[ngram_start] in IGNORED_CHARS:
            return ""
        if ngram_length <= 0:
            return ""
        if ngram_start + ngram_length >= len(txt):
            return ""

        ngram = txt[ngram_start : ngram_start + ngram_length]

        for n in ngram[1:]:  # 1st char already tested
            if n in IGNORED_CHARS:
                return ""

        return ngram

    # get all n-grams
    for ngram_start in range(len(txt)):
        for ngram_length in range(NGRAM_MAX_LENGTH):
            _ngram = get_ngram(txt, ngram_start, ngram_length)

            if not _ngram:  # _ngram is ""
                continue

            if _ngram not in ngrams[ngram_length]:
                ngrams[ngram_length][_ngram] = 0

            ngrams[ngram_length][_ngram] += 1
            ngrams_count[ngram_length] += 1

    # sort the dictionary by symbol frequency (requires CPython 3.6+)
    def sort_by_frequency(table: dict, char_count: int, precision: int = 3) -> dict:
        sorted_dict = {}
        for key, count in sorted(table.items(), key=lambda x: -x[1]):
            freq = round(100 * count / char_count, precision)
            if freq > 0:
                sorted_dict[key] = freq
        return sorted_dict

    for ngram in range(1, NGRAM_MAX_LENGTH):
        ngrams[ngram] = sort_by_frequency(ngrams[ngram], ngrams_count[ngram], 4)

    return ngrams, ngrams_count


def read_corpus(file: Path, name: str = "", encoding="utf-8") -> dict:
    """read a .txt file and provide a dictionary of n-grams"""
    try:
        if not file.is_file:
            raise Exception("Error, this is not a file")
        if not name:
            name = file.stem
        with file.open("r", encoding=encoding) as f:
            corpus_txt = "↵".join(f.readlines())

    except Exception as e:
        print(f"file does not exist or could not be read.\n {e}")

    ngrams_freq, ngrams_count = parse_corpus(corpus_txt)
    return {
        "name": name,
        "freq": ngrams_freq,
        "count": ngrams_count,
    }


if __name__ == "__main__":
    if len(argv) == 2:  # convert one file
        file = Path(argv[1])
        data = read_corpus(file)
        output_file_path = file.parent / f"{file.stem}.json"
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        print(json.dumps(data, indent=4, ensure_ascii=False))

    else:  # converts all *.txt files in the script directory
        txt_dir = Path(__file__).resolve().parent.parent / "txt"
        for file in sorted(txt_dir.glob("*.txt")):
            if file.is_file():
                print(f"...  {file.stem}")
                data = read_corpus(file)
                output_file_path = txt_dir / f"{file.stem}.json"
                with open(output_file_path, "w", encoding="utf-8") as outfile:
                    json.dump(data, outfile, indent=4, ensure_ascii=False)
