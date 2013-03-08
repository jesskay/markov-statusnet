#!/usr/bin/env python
import random


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
                markov_table[tuple(ngram[:-1])] = []
            markov_table[tuple(ngram[:-1])].append(ngram[-1])

    return markov_table


def generate_output(markov_table, start_marker=None, end_marker=None,
        max_length=0):
    keys = list(markov_table.keys())
    ngram_size = len(keys[0])
    source_is_string = isinstance(list(markov_table.keys())[0], str)

    if start_marker is None:
        start = random.choice(keys)
    else:
        start = random.choice(list(filter((lambda x: x[0] == start_marker), keys)))

    if source_is_string:
        output = start
    else:
        output = list(start)

    while (max_length == 0) or (len(output) < max_length):
        if source_is_string:
            next_piece = random.choice(markov_table[output[(0-ngram_size):]])
        else:
            next_piece = random.choice(markov_table[tuple(output[(0-ngram_size):])])

        if next_piece == end_marker:
            break
        else:
            if source_is_string:
                output += next_piece
            else:
                output.append(next_piece)

    if start_marker is not None:
        if source_is_string:
            output = output.replace(start_marker, "", 1)
        else:
            output = output[1:]

    return output
