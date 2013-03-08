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
