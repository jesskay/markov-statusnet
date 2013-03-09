#!/usr/bin/env python
import requests, os, sys, pickle


def fetch_notices(username, host, use_https=False):
    """Fetches all notices for a given user at a given host."""
    last_id = 0
    notices = {}
    while True:
        try:
            new_notices = requests.get("{protocol}://{host}/api/statuses/user_timeline.json".format(
                    protocol="https" if use_https else "http",
                    host=host),
                params={
                    "screen_name": username,
                    "max_id": str(last_id - 1)
                    })
        except requests.exceptions.ConnectionError:
            sys.stderr.write("GET failed with a connection error. Aborting " +
                    "prematurely.\n")
            break

        if new_notices.status_code == 200:
            new_notice_data = new_notices.json()
        elif (new_notices.status_code >= 400) and (new_notices.status_code <
                500):
            sys.stderr.write("GET failed with a 4xx error. Aborting " +
                    "prematurely.\n")
            break
        else:
            sys.stderr.write("GET failed. If you're seeing this a lot, something may be wrong.\n")
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
        os.mkdir(host)
    except OSError:
        pass  # Directory already exists, don't care.
    try:
        with open("{0}/{1}.picklejar".format(host, username), "wb") as picklejar:
            pickle.dump(notices, picklejar)
    except IOError:
        sys.stderr.write("WARNING: Couldn't pickle notices. The script will" +
                " most likely still work, but this may result in inefficient" +
                " operation.\n")

    return notices
