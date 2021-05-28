#!/usr/bin/env python

import argparse
import json
import sys
import time
from   urllib.error import HTTPError
import urllib.request

API = "https://overpass-api.de/api/interpreter"

# Ratelimit config (values in minutes)
# Depending on how busy the server is, you could be ratelimited very quickly
# See https://github.com/drolbr/Overpass-API/issues/333#issuecomment-256693066
RATELIMIT_INIT = 1
RATELIMIT_BACKOFF_FACTOR = 2
RATELIMIT_MAX_TIME = 15
RATELIMIT_MAX_RETRY = 10


def eprint(*args, **kwargs):
    # Don't add a newline for messages ending with "..."
    if args and args[0].endswith("...") and not "end" in kwargs:
        kwargs["end"] = ""
        kwargs["flush"] = True
    print(*args, file=sys.stderr, **kwargs)


def get_json(*args, **kwargs):
    for x in range(RATELIMIT_MAX_RETRY):
        try:
            with urllib.request.urlopen(*args, **kwargs) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as e:
            if e.code not in (429, 504) or x >= RATELIMIT_MAX_RETRY - 1:
                raise
            delay = min(RATELIMIT_INIT * (RATELIMIT_BACKOFF_FACTOR ** x), RATELIMIT_MAX_TIME)
            if x == 0:
                eprint(f"hit ratelimit, retry in {delay} min...")
            else:
                eprint(f"in {delay} min...")
            time.sleep(delay * 60)


def call_api(query):
    time.sleep(1)
    return get_json(f"{API}?data=[out:json];{query};out+tags+center;")


def elm_data(elm, lang=None):
    name = None
    if lang:
        name = elm["tags"].get(f"name:{lang}")
    if not name:
        name = elm["tags"].get("name")
    return {
        "name": name,
        "lat": elm.get("center", {}).get("lat"),
        "lon": elm.get("center", {}).get("lon"),
    }


def get_elements(data, code_key, lang=None):
    seen = set()
    for e in data["elements"]:
        code = e["tags"][code_key]
        if code not in seen:
            seen.add(code)
            yield code, elm_data(e, lang=lang)


def get_3166_1(lang=None):
    eprint("Getting all country code data...")
    data = call_api("relation['ISO3166-1'~'.*']")
    eprint(f"done ({len(data['elements'])} countries)")

    yield from get_elements(data, "ISO3166-1", lang=lang)


def get_3166_2(code, lang=None):
    eprint(f"Getting region data for {code}...")
    data = call_api(f"relation['ISO3166-2'~'^{code}-']")
    eprint(f"done ({len(data['elements'])} regions)")

    yield from get_elements(data, "ISO3166-2", lang=lang)


def get_3166(lang=None):
    for c_code, c_data in get_3166_1(lang=lang):
        yield c_code, c_data
        yield from get_3166_2(c_code, lang=lang)


def main():
    parser = argparse.ArgumentParser(description="Get ISO 3166 data from OpenStreetMap")
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        help="Where to output the results (default: %(default)s)",
        required=False,
        default="-",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="The 2-letter language code (ISO 639-1) to prefer for place names (default: untranslated)",
        required=False,
        default=None,
    )
    args = parser.parse_args()

    data = dict(get_3166(lang=args.language))

    eprint(f"Writing data for {len(data)} countries and regions...")
    with args.output as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    eprint("done!")


if __name__ == "__main__":
    main()
