"""imports or reads your raw dataset; if you scraped, include scraper here"""
from google_play_scraper import app, reviews_all, Sort
import pandas as pd
import numpy as np
import json

reviews = reviews_all(
    'com.getsomeheadspace.android',
    sleep_milliseconds=0, # defaults to 0
    lang='en', # defaults to 'en'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
) 

reviews = reviews[:2500]

with open("../data/reviews_raw.jsonl", "a", encoding="utf-8") as f:
   for review in reviews:
    review["at"] = review["at"].isoformat()
    f.write(json.dumps(review, ensure_ascii=False, default=str) + "\n")
