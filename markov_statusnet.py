#!/usr/bin/env python
import markov, notices, sys, argparse

markers = {
        "start_marker": type("StartMarker", (object,), {}),
        "end_marker": type("EndMarker", (object,), {}),
        }


def split_uri(target_uri):
    """Splits a URI of the format [acct:]username@host into its components."""
    if target_uri[:5] == "acct:":
        target_uri = target_uri[5:]
    username, host = target_uri.split("@")
    return (username, host)


def main():
    arg_parser = argparse.ArgumentParser(description="""Generate nonsense based
            on a StatusNet user's notices.""")
    arg_parser.add_argument("-f", "--force-fetch", action="store_true",
            help="""Force the notices to be fetched, even if a cached copy
            exists.""", dest="force_fetch")
    arg_parser.add_argument("-s", "--use-https", action="store_true",
            help="""Use HTTPS to fetch notices.""", dest="use_https")
    arg_parser.add_argument("-n", "--nonsense-count", dest="nonsense_count",
            type=int, help="""Number of nonsense notices to generate per
            user.""", default=1)
    arg_parser.add_argument("-p", "--prefix-length", dest="prefix_length",
            type=int, help="""Size of prefix to use (internally, ngrams will be
            this + 1). Generally, lower sizes => more randomness.""", default=2)
    arg_parser.add_argument("users", metavar="USER@HOST", nargs="+",
            help="""User to generate nonsense notices for.""")

    args = arg_parser.parse_args()

    for user in args.users:
        try:
            username, host = split_uri(user)
        except ValueError:
            sys.stderr.write("User given in invalid format: {0}\n. Skipping.\n")
            continue

        user_notices = notices.get_notices(username, host, args.use_https,
                args.force_fetch)

        if user_notices == []:
            sys.stderr.write("No notices fetched. Cannot generate nonsense.\n")
            sys.exit(1)

        user_markov_table = {}
        for notice in user_notices:
            ngrams = markov.make_ngrams(notice.split(), n=args.prefix_length,
                    **markers)
            user_markov_table = markov.make_markov_table(ngrams,
                    user_markov_table)

        for i in range(0, args.nonsense_count):
            while True:
                nonsense = " ".join(markov.generate_output(user_markov_table,
                    **markers))
                if not nonsense in user_notices:
                    break
            print(nonsense)


if __name__ == "__main__":
    main()
