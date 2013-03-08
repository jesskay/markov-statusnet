#!/usr/bin/env python
import requests, sys

def split_uri(target_uri):
    if target_uri[:5] == "acct:":
        target_uri = target_uri[5:]
    username, host = target_uri.split("@")
    return (username, host)

def get_notices(username, host, use_https=False):
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

    return notices.values()

# TODO: turn the list of notices into a markov table
# TODO: generate stuff based on the table
