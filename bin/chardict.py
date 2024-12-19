#!/usr/bin/env python3
"""Turn corpus texts into dictionaries of symbols, bigrams and trigrams."""

import json
from os import listdir, path
from sys import argv
import platformdirs

IGNORED_CHARS = "1234567890 \t\r\n\ufeff"


def parse_corpus(file_path):
    """Count symbols, bigrams and trigrams in a text file."""

    symbols = {}
    bigrams = {}
    trigrams = {}
    char_count = 0
    prev_symbol = None
    prev_prev_symbol = None

    # get a dictionary of all symbols (letters, punctuation marks...)
    file = open(file_path, "r", encoding="utf-8")
    for char in file.read():
        symbol = char.lower()
        if char not in IGNORED_CHARS:
            char_count += 1
            if symbol not in symbols:
                symbols[symbol] = 0
            symbols[symbol] += 1
            if prev_symbol is not None:
                bigram = prev_symbol + symbol
                if bigram not in bigrams:
                    bigrams[bigram] = 0
                bigrams[bigram] += 1
                if prev_prev_symbol is not None:
                    trigram = prev_prev_symbol + bigram
                    if trigram not in trigrams:
                        trigrams[trigram] = 0
                    trigrams[trigram] += 1
            prev_prev_symbol = prev_symbol
            prev_symbol = symbol
        else:
            prev_symbol = None
    file.close()

    # sort the dictionary by symbol frequency (requires CPython 3.6+)
    def sort_by_frequency(table, precision=3):
        sorted_dict = {}
        for key, count in sorted(table.items(), key=lambda x: -x[1]):
            freq = round(100 * count / char_count, precision)
            if freq > 0:
                sorted_dict[key] = freq
        return sorted_dict

    results = {}
    results["corpus"] = file_path
    results["symbols"] = sort_by_frequency(symbols)
    results["bigrams"] = sort_by_frequency(bigrams, 4)
    results["trigrams"] = sort_by_frequency(trigrams)
    return results


def add(file_path: str, name: str = "", encoding="utf-8"):
    corpus = read_corpus(file_path, name, encoding)
    if corpus is not None:
        data_path = Path(platformdirs.user_config_dir(APP_NAME, APP_AUTHOR)) / "corpora"
        data_path.mkdir(parents=True, exist_ok=True)
        data_path = data_path / f"{corpus["name"]}.json"
        try:
            with data_path.open("w", encoding="utf-8") as outfile:
                json.dump(corpus, outfile, indent=4, ensure_ascii=False)
                print(f"Corpus “{corpus['name']}” added to {data_path}")
        except:
            print(f"Error: could not write to {data_path}")


def rm(name: str):
    corpus_path = Path(platformdirs.user_config_dir(APP_NAME, APP_AUTHOR)) / "corpora"
    corpus_path = corpus_path / f"{name}.json"
    try:
        corpus_path.unlink()
        print(f"Corpus “{name}” deleted")
    except FileNotFoundError:
        print(f"Corpus “{name}” does not exist")


if __name__ == "__main__":
    if len(argv) == 2:  # convert one file
        data = parse_corpus(argv[1])
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:  # converts all *.txt files in the script directory
        bin_dir = path.dirname(__file__)
        destdir = path.join(bin_dir, "..", "txt")
        txtdir = path.join(bin_dir, "..", "txt")
        for filename in listdir(txtdir):
            if filename.endswith(".txt"):
                basename = filename[:-4]
                print(f"...  {basename}")
                data = parse_corpus(path.join(txtdir, filename))
                destfile = path.join(destdir, basename + ".json")
                with open(destfile, "w", encoding="utf-8") as outfile:
                    json.dump(data, outfile, indent=4, ensure_ascii=False)
