import bisect
import math
import os.path
import random
from contextlib import asynccontextmanager
from enum import IntEnum
from typing import Annotated

from fastapi import FastAPI, Query


# Mutation types must be defined in order of application
class Mutation(IntEnum):
    SWITCH = 1
    SUPERSWITCH = 2
    FLIP = 3
    DELETE = 4


# List out mutations along with their cumulative probabilities for
# selection
MUTATION_SELECTOR = [
    (Mutation.SWITCH, 0.8),  # p = 0.8
    (Mutation.SUPERSWITCH, 0.85),  # p = 0.05
    (Mutation.FLIP, 0.95),  # p = 0.1
    (Mutation.DELETE, 1.0),  # p = 0.05
]


# Return a mutation based on a random selector
def select_mutation(r: float) -> Mutation:
    for mutation, cum_prob in MUTATION_SELECTOR:
        if r < cum_prob:
            return mutation
    raise ValueError("Invalid random value for mutation selection")


# Locations of compiled data files
DATA_DIR = "compiled-data"
LASTNAME_FILE = os.path.join(DATA_DIR, "all_last.txt")
FEMALE_FILE = os.path.join(DATA_DIR, "female_first.txt")
MALE_FILE = os.path.join(DATA_DIR, "male_first.txt")

# Additional configuration
BASE_MUTATE_COUNT = 2
FEMALE_NAME_P = 0.1
EXTRA_MUTATE_P = 0.2

VOWELS = "AEIOU"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ"
LETTERS = VOWELS + CONSONANTS

# In-memory storage for name data
lastnames: list[tuple[str, float]] = []
female_names: list[tuple[str, float]] = []
male_names: list[tuple[str, float]] = []


def bisect_name(name_list: list[tuple[str, float]], r: float) -> str:
    idx = bisect.bisect_right(name_list, r, key=lambda x: x[1])
    return name_list[idx][0]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    with open(LASTNAME_FILE, "r") as f:
        for line in f:
            (name, prob) = line.split()
            lastnames.append((name, float(prob)))
    if not math.isclose(lastnames[-1][1], 1.0):
        raise ValueError("Last names cumulative probability does not sum to 1.0")
    with open(FEMALE_FILE, "r") as f:
        for line in f:
            (name, prob) = line.split()
            female_names.append((name, float(prob)))
    if not math.isclose(female_names[-1][1], 1.0):
        raise ValueError("Female names cumulative probability does not sum to 1.0")
    with open(MALE_FILE, "r") as f:
        for line in f:
            (name, prob) = line.split()
            male_names.append((name, float(prob)))
    if not math.isclose(male_names[-1][1], 1.0):
        raise ValueError("Male names cumulative probability does not sum to 1.0")
    yield
    # Shutdown code here


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/dugnutt")
async def dugnutt(count: Annotated[int, Query(gt=0, lt=1025)] = 1):
    results = []
    for _ in range(count):
        lastname = bisect_name(lastnames, random.random())
        if random.random() < FEMALE_NAME_P:
            firstname = bisect_name(female_names, random.random())
        else:
            firstname = bisect_name(male_names, random.random())
        mutation_count = BASE_MUTATE_COUNT
        max_mutations = len(firstname) + len(lastname)
        while random.random() < EXTRA_MUTATE_P and mutation_count <= max_mutations:
            mutation_count += 1
        # Cap max_mutations in case the string is shorter than BASE_MUTATE_COUNT
        mutation_count = min(mutation_count, max_mutations)
        # Generate the list of mutations to perform, sorted first by mutation
        # type and then by descending position to avoid index shifting issues
        mutations = sorted(
            zip(
                map(select_mutation, [random.random() for _ in range(mutation_count)]),
                random.sample(range(max_mutations), mutation_count),
            ),
            key=lambda x: (x[0].value, -x[1]),
        )
        output_chars = list(firstname + " " + lastname)
        for mutation, pos in mutations:
            if pos >= len(firstname):
                pos += 1  # Skip the space between first and last name
            match mutation:
                case Mutation.SWITCH:
                    if output_chars[pos] in VOWELS:
                        candidates = VOWELS.replace(output_chars[pos], "")
                    else:
                        candidates = CONSONANTS.replace(output_chars[pos], "")
                    output_chars[pos] = random.choice(candidates)
                case Mutation.SUPERSWITCH:
                    output_chars[pos] = random.choice(
                        LETTERS.replace(output_chars[pos], "")
                    )
                case Mutation.FLIP:
                    dst_pos = pos + 1 if pos < len(output_chars) - 1 else 0
                    (output_chars[pos], output_chars[dst_pos]) = (
                        output_chars[dst_pos],
                        output_chars[pos],
                    )
                case Mutation.DELETE:
                    # This is only safe because we sorted by descending position!
                    del output_chars[pos]
        results.append("".join(output_chars))
    return {"names": results}
