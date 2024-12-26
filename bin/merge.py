#!/usr/bin/env python3
"""Merge several corpus dictionaries."""

import json
from sys import argv
from pathlib import Path


# sort the merged dictionary by symbol frequency (requires CPython 3.6+)
def _sort_ngram_by_frequency(table, precision=3):
    sorted_dict = {}
    for key, count in sorted(table.items(), key=lambda x: -x[1]):
        freq = round(count, precision)
        if freq > 0:
            sorted_dict[key] = freq
    return sorted_dict


def sort_by_frequency(corpus: dict, precision=3):
    for index in range(1, len(corpus["freq"].keys())+1):
        ngram = str(ngram)
        corpus["freq"][ngram] = _sort_ngram_by_frequency(
            corpus["freq"][ngram], precision
        )
    return corpus

def read_corpora(filenames: list[Path]) -> list[dict]:
    """open a collection of corpus from path and dump its content in a dictionary"""
    corpora = []
    for filename in filenames:
        try:
            with open(filename) as f:
                corpus = json.load(f)
                corpora.append(corpus)
        except:
            print(
                f"Warning: cannot open the `{filename.stem}` corpus; skipping this file"
            )
            continue
    return corpora

def mergeable(corpora:list[dict]) -> bool:
    """check if corpora cam be merge (n-gram of same length)"""
    error_str = "Error: at least 2 corpuses are needed to merge, aborting"
    if len(corpora) < 2:
        print(error_str)
        return False

    # removing corpus that do not have the same ngram length
    ngram_length = len( corpora[0]["freq"] )
    corpora_initial_length = len(corpora)
    corpora = [corpus for corpus in corpora if len(corpus["freq"]) == ngram_length]
    if len(corpora) != corpora_initial_length:
        print(f"Error: cannot merge because corpus file format is different; all corpuses do not have the same ngram length")
    
    if len(corpora) >= 2:
        return True

    print(error_str)
    return False

def mix(corpora:list[dict], name:str="mixed", weights:list[float]=None) -> dict:
    """merge corpora of same n-gram length, optionally with a given set of weight"""
    weights = weights or []
    if weights == []:
        # merge with same weight by default
        weights = [ 1/len(corpora) ] * len(corpora)
    elif round(sum(weights),1) != 1:
        print("Error: provided merge ratio do not add-up to 1; aborting merge")

    ngram_length = range(1, len(corpora[0]["freq"].keys()) +1)

    output_corpus = {
        "freq": {str(n):{} for n in ngram_length},
        "count": {str(n):0 for n in ngram_length},
    }

    for index in ngram_length:
        n = str(index)
        for corpus_index, corpus in enumerate(corpora):
            output_corpus["count"][n] += corpus["count"][n]
            for ngram in corpus["freq"][n]:
                if ngram not in output_corpus["freq"][n]:
                    output_corpus["freq"][n][ngram] = 0
                output_corpus["freq"][n][ngram] += corpus["freq"][n][ngram] * weights[corpus_index]
    return output_corpus



if __name__ == "__main__":
    argl = len(argv) - 1  # number of files to merge
    if argl >= 2:
        dir = Path(__file__).resolve().parent.parent
        files = [Path(f) for f in argv[1:]]
        corpora = read_corpora(files)
        if not mergeable(corpora):
            print("Error: cannot merge corpora, aborting")
            exit()
        name = "mixed"
        corpus = mix(corpora, name=name)
        with open(f"{name}.json", "w", encoding="utf-8") as outfile:
            json.dump(corpus, outfile, indent=4, ensure_ascii=False)
        print(json.dumps(corpus, indent=4, ensure_ascii=False))
