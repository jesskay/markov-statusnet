#!/usr/bin/env python


def split_uri(target_uri):
    """Splits a URI of the format [acct:]username@host into its components."""
    if target_uri[:5] == "acct:":
        target_uri = target_uri[5:]
    username, host = target_uri.split("@")
    return (username, host)


def make_ngrams(orig_source, n=2, end_marker=None):
    source = orig_source[:]  # Don't want to modify original if given a reference

    if end_marker is not None:
        if isinstance(source, str):
            source += end_marker
        else:
            source.append(end_marker)

    for i in range(0, len(source) - (n - 1)):
        yield source[i:i+n]


# TODO: turn the list of notices into a markov table
# TODO: generate stuff based on the table
