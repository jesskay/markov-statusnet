#!/usr/bin/env python


def make_ngrams(orig_source, n=2, end_marker=None):
    source = orig_source[:]  # Don't want to modify original if given a reference

    if end_marker is not None:
        if isinstance(source, str):
            source += end_marker
        else:
            source.append(end_marker)

    for i in range(0, len(source) - (n - 1)):
        yield source[i:i+n]
