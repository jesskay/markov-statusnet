#!/usr/bin/env python
import requests, sys, pickle


def split_uri(target_uri):
    """Splits a URI of the format [acct:]username@host into its components."""
    if target_uri[:5] == "acct:":
        target_uri = target_uri[5:]
    username, host = target_uri.split("@")
    return (username, host)


def fetch_notices(username, host, use_https=False):
    """Fetches all notices for a given user at a given host."""
    last_id = 0
    notices = {}
    while True:
        new_notices = requests.get("{protocol}://{host}/api/statuses/user_timeline.json".format(
                protocol="https" if use_https else "http",
                host=host),
            params={
                "screen_name": username,
                "max_id": str(last_id - 1)
                })

        if new_notices.status_code == 200:
            new_notice_data = new_notices.json()
        else:
            sys.stderr.write("GET failed. If you're seeing this a lot, something may be wrong.")
            continue

        if new_notice_data == []:
            break
        else:
            for notice in new_notice_data:
                notices[int(notice["id"])] = notice["text"]
                last_id = int(notice["id"])

        if last_id == 1:
            break  # Just fetched id 1. Done either way.

    return list(notices.values())


def get_notices(username, host, use_https=False, force_fetch=False):
    if not force_fetch:
        try:
            with open("{0}/{1}.picklejar".format(host, username), "rb") as picklejar:
                return pickle.load(picklejar)
        except IOError:  # file bad or nonexistent
            pass         # so we'll fetch

    notices = fetch_notices(username, host, use_https)

    try:
        with open("{0}/{1}.picklejar".format(host, username), "wb") as picklejar:
            pickle.dump(notices, picklejar)
    except IOError:
        sys.stderr.write("WARNING: Couldn't pickle notices. The script will " +
                "still work, but this will result in inefficient operation.")

    return notices


# TODO: turn the list of notices into a markov table
# TODO: generate stuff based on the table
