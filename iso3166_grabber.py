#!/usr/bin/env python

import argparse
import json
import sys
import urllib.request

API = "https://lz4.overpass-api.de/api/interpreter"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_json(*args, **kwargs):
    with urllib.request.urlopen(*args, **kwargs) as r:
        return json.loads(r.read().decode("utf-8"))


def call_api(query):
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
    eprint("Getting all country code data...", end="", flush=True)
    data = call_api("relation['ISO3166-1'~'.*']")
    eprint(f"done ({len(data['elements'])} countries)")

    yield from get_elements(data, "ISO3166-1", lang=lang)


def get_3166_2(code, lang=None):
    eprint(f"Getting region data for {code}...", end="", flush=True)
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

    eprint(f"Writing data for {len(data)} countries and regions...", end="", flush=True)
    with args.output as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    eprint("done!")


if __name__ == "__main__":
    main()
