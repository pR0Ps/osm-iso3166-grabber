OpenStreetMap ISO 3166 Grabber
==============================

Get ISO 3166 data from OpenStreetMap

Installation
------------
Use `pip` to install (preferably into a virtual environment):

```bash
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install git+https://github.com/pR0Ps/osm-iso3166-grabber.git
```

Usage
-----
```bash
$ iso3166-grabber --help
usage: iso3166-grabber [-h] [-o OUTPUT] [-l LANGUAGE]

Get ISO 3166 data from OpenStreetMap

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Where to output the results (default: -)
  -l LANGUAGE, --language LANGUAGE
                        The 2-letter language code (ISO 639-1) to prefer for
                        place names (default: untranslated)
```

Output
------
The output will be formatted as JSON with the following structure:
```json
{
    "CA": {
        "lat": 62.5063842,
        "lon": -96.6629741,
        "name": "Canada"
    },
    "CA-AB": {
        "lat": 54.4985442,
        "lon": -115.0030737,
        "name": "Alberta"
    }
}
```

Licenses
========
Licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

The data collected by this tool from OpenStreetMap is licensed under the
[ODbL](https://opendatacommons.org/licenses/odbl/). See <https://www.openstreetmap.org/copyright>
for details.
