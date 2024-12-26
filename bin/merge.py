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
    for ngram in range(1, len(corpus["freq"].keys())+1):
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

    # removing corpus that do not have the same ngram lenght
    ngram_length = len( corpora[0]["freq"] )
    removed_corpuses = [corpus["name"] for corpus in corpora if len(corpus["freq"]) != ngram_length]
    corpora = [corpus for corpus in corpora if len(corpus["freq"]) == ngram_length]
    for _name in removed_corpuses:
        print(f"Warning: removing {_name} from corpora because ngram length is different")
    
    if len(corpora) >= 2:
        return True

    print(error_str)
    return False

def mix(corpora:list[dict], name:str="mixed", ratio:list[float]=[]) -> dict:
    """merge corpora of same n-gram length, optionally with a giver ratio"""
    if ratio == []:
        # merge with same weight by default
        ratio = [ 1/len(corpora) ] * len(corpora)
    elif round(sum(ratio),1) != 1:
        print("Error: provided merge ratio do not add-up to 1; aborting merge")

    output_corpus = corpora[0].copy()
    output_corpus["name"] = name

    # manage 1st corpus
    for index in output_corpus["freq"]:
        n = str(index)
        for ngram in output_corpus["freq"][n]:
            output_corpus["freq"][n][ngram] *= ratio[0]

    # manage others
    for index in range(1, len(output_corpus["freq"].keys()) +1):
        n = str(index)
        for corpus_index, corpus in enumerate(corpora[1:]):
            print(corpus, corpus_index)
            output_corpus["count"][n] += corpus["count"][n]

            for ngram in corpus["freq"][n]:
                if ngram not in output_corpus["freq"][n]:
                    output_corpus["freq"][n][ngram] = 0
                output_corpus["freq"][n][ngram] += corpus["freq"][n][ngram] * ratio[corpus_index]
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
        corpus = mix(corpora, name="mixed")
        with open(f"{corpus["name"]}.json", "w", encoding="utf-8") as outfile:
            json.dump(corpus, outfile, indent=4, ensure_ascii=False)
        print(json.dumps(corpus, indent=4, ensure_ascii=False))
