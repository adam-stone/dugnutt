## Dugnutt: A Fighting-Baseball-inspired roster generator

Dugnutt is a web toy inspired by the rosters from the 1994 Japanese
baseball game
[Fighting Baseball for the Super NES](https://en.wikipedia.org/wiki/MLBPA_Baseball),
which famously included rosters composed of player names constructed from a
kind of mangled hash of various baseball and hocker players of the time.

My official deployment of this toy lives at <https://straythought.xyz/toys/dugnutt.html>

## How it works

This toy operates on a [dataset of name frequencies from the 1990 U.S. Census](https://www.census.gov/topics/population/genealogy/data/1990_census/1990_census_namefiles.html).

The backend loads this data, including each name's relative frequency. When
generating a new roster name, it selects a surname weighted by frequency.
It selects whether to pull a given name from the list of male or female names
and then chooses from that list weighted by frequency.

Once a pair of names is selected, it randmoly "mutates" each name at least
twice and no more than the total number of letters in the full name. Each
mutation changes a single letter in the name by either:
- Replacing a letter with another letter of its type (vowel or consonant)
- Replacing a letter with another letter without regard for type
- Swapping adjancent characters (including the space between names)
- Deleting a letter

The app includes a simple frontend written in Svelte that requests a set of
names from the backend and renders them nicely.

## Build instructions

### Building data

The data has been precompiled and checked into the repo, but it can be rebuilt
from similarly-formatted source data using the script in the tools/ directory:

```
python compile-data.py data/dist.all.last.txt > compiled-data/all_last.txt
python compile-data.py data/dist.female.first.txt > compiled-data/female_first.txt
python compile-data.py data/dist.male.first.txt > compiled-data/male_first.txt
```

### Building the front end

From the root directory, build the frontend as follows:

```
cd frontend
npm install
npm run build
```

### Building and running the server

Once the data and front end have been built, the server can be started. If you
want to pre-install dependencies, you can start with

```
uv sync --frozen
```

Or you run the server directly with
```
uv run fastapi dev server.py
```

In deployment, run the server through uvicorn as follows:
```
uv run uvicorn server:app
```

using the --host and --port arguments according to deploy target requirements


## Author
Adam Stone
<https://straythought.xyz/>
