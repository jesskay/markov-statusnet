#!/usr/bin/env python
import markov, notices


def split_uri(target_uri):
    """Splits a URI of the format [acct:]username@host into its components."""
    if target_uri[:5] == "acct:":
        target_uri = target_uri[5:]
    username, host = target_uri.split("@")
    return (username, host)


# TODO: turn the list of notices into a markov table
# TODO: generate stuff based on the table
