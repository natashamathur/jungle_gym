import re
import time
import pandas as pd
import wikipediaapi

wiki = wikipediaapi.Wikipedia("en")

import nltk

nltk.download("wordnet")
from nltk.corpus import wordnet as wn
from datetime import datetime, timedelta
import urllib.request
import jellyfish as jf
import requests
from bs4 import BeautifulSoup

from occupational_dictionary import occ_dict

# Access Wikipedia API


def run_wikipedia_api(df, unique_id="email"):
    """Runs through a pandas dataframe and makes a dictionary of all unique_ids and bios found"""

    wiki_dict = {}

    for i, row in df.iterrows():

        if i % 5000 == 0 and i > 0:
            print("taking a nap @", i, datetime.now().strftime("%b %d %Y %H:%M:%S"))
            time.sleep(30)
            print("woke up", datetime.now().strftime("%b %d %Y %H:%M:%S"))

        if i % 1000 == 0 and i % 5000 != 0:
            print(i, datetime.now().strftime("%b %d %Y %H:%M:%S"))

        page = wiki.page(str(row.full_name))

        if page:
            try:
                bio = page.summary.split(".")[0]
                wiki_dict[row[unique_id]] = {"name": row.full_name, "bio": bio}
            except Exception as e:
                print("Exception", e)

    return wiki_dict


def get_wiki_info(unique_id, info, wiki_dict):
    """Applies information from wikipedia onto pandas dataframe."""
    if unique_id in wiki_dict.keys():
        return wiki_dict[unique_id][info]
    else:
        return ""


# Match occupations to wikipedia description


def classify(occupation, occ_dict):
    """Checks if occupation in board dictionary of occupation categories."""
    cats = []
    if type(occupation) == str:
        occupation = occupation.split()
    for o in occupation:
        if o in occ_dict.keys():
            cats.append(occ_dict[o])
    return cats


def extract_occ(s):
    """Parses bio summary based on common sentence structures to try extract occupation."""
    try:
        s = re.split(" [a-z]{2}[.] ", s)
        s = s[0].split(" is ")[1]
        s = re.split("known |whose |who |specializing ", s)[0]
        s = s.split()
        s = [
            x.strip(",|.").lower()
            for x in s
            if x
            not in ["an", "American", "n", "professional", "former", "and", "the", "a"]
        ]
        return s
    except Exception:
        return []


def check_match(x, y):
    for i in x:
        for j in y:
            if i == j:
                return True

    return False


def get_score(o1, o2):
    """Calculates the path similarity between the provided occupation and the Wikipedia occupation 
        based on hypernym/hyponym taxonomy."""

    score = 0
    if "self" in o1.lower():
        return 0.5
    try:
        if type(o1) == str:
            o1 = o1.split()
        for x in o1:
            for y in o2:
                try:
                    sc = wn.synsets(x)[0].path_similarity(wn.synsets(y)[0])
                except:
                    sc = None

                if sc != None and sc > score:
                    score = sc
        return score
    except Exception as e:
        return -1


def check_names(first, last, wiki_name):
    """Ensure that wikipedia name and provided name match."""

    wn = wiki_name.split(" ")
    wiki_first, wiki_last = wn[0], wn[-1]

    if (
        jf.jaro_winkler(last, wiki_last) < 0.95
        or jf.jaro_winkler(first, wiki_first) < 0.95
    ):
        return False
    return True


def find_matches(names):
    """Checks whether provided occupation matches the Wikipedia description
        to determine whether this is an accurate match."""

    # Classifies provided occupation
    names["occ_cat"] = names.occupation.apply(lambda x: classify(x, occ_dict))

    # Extracts occupation from Wikipedia bio and categories as above.
    names["wiki_occ"] = names.wiki_bio.apply(extract_occ,)
    names["wiki_cat"] = names.wiki_occ.apply(lambda x: classify(x, occ_dict))

    # Checks for an exact match between occupational categories
    names["is_match"] = names[["occ_cat", "wiki_cat"]].apply(
        lambda x: check_match(*x), axis=1
    )

    # Calculates path similarity between occupations.
    names["occ_match_score"] = names[["occupation", "wiki_occ"]].apply(
        lambda x: get_score(*x), axis=1
    )

    # Check that wikipedia name and provided name match.
    names["name_check"] = names[["firstname", "lastname", "wiki_name"]].apply(
        lambda x: check_names(x[0], x[1], x[2]), axis=1
    )

    """
    Narrow down to people who have a wikipedia-derived occupation and  at least a moderate path similarity.
    """
    names_proc = names_proc[
        (occ_match_score.score > 0.3) & (len(names.wiki_occ) > 0)
    ].copy()

    """
    People who either 1) have exactly matched categories or 2) have a higher path similarity between occupations 
    """
    names_proc = names.loc[
        (names.is_match == True) | (names.occ_match_score > 0.5)
    ].copy()

    # Confirm that name match
    names_proc = names_proc[names_proc.name_check == True].copy()

    # Confirm that the person is American
    names_proc = names_proc[
        ~names_proc.wiki_bio.str.contains("British|Canadian|Scottish|English")
    ].copy()

    # Get url for matched names
    names_proc["wiki_url"] = names_proc.wiki_name.apply(
        lambda x: "https://en.wikipedia.org/wiki/{}".format(wn.replace(" ", "_"))
    )

    # Remove processing columns
    names_proc = names_proc.drop(
        ["occ_cat", "wiki_cat", "is_match", "occ_match_score", "name_check"]
    )

    print(f"There were {len(names_proc)} matches found.")

    return names_proc
