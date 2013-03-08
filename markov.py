#!/usr/bin/env python


def make_ngrams(orig_source, n=2, start_marker=None, end_marker=None):
    source = orig_source[:]  # Don't want to modify original if given a reference

    if start_marker is not None:
        if isinstance(source, str):
            source = start_marker + source
        else:
            source.insert(0, start_marker)

    if end_marker is not None:
        if isinstance(source, str):
            source += end_marker
        else:
            source.append(end_marker)

    for i in range(0, len(source) - n):
        yield source[i:i+n+1]


def make_markov_table(ngrams, preset_table={}):
    markov_table = preset_table

    for ngram in ngrams:
        if isinstance(ngram, str):
            if not ngram[:-1] in markov_table:
                markov_table[ngram[:-1]] = []
            markov_table[ngram[:-1]].append(ngram[-1])
        else:
            if not tuple(ngram[:-1]) in markov_table:
                markov_table[ngram[:-1]] = []
            markov_table[tuple(ngram[:-1])].append(ngram[-1])

    return markov_table
