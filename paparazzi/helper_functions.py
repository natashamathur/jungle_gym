import re
import time
import pandas as pd
from helper_functions import *
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

def run_wikipedia_api(df, unique_id='email'):
    '''Runs through a pandas dataframe and makes a dictionary of all unique_ids and bios found'''

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
    '''Applies information from wikipedia onto pandas dataframe.'''
    if unique_id in wiki_dict.keys():
        return wiki_dict[unique_id][info]
    else:
        return ""