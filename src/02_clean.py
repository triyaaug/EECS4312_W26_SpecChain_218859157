"""cleans raw data & make clean dataset"""
import json
import re
import os
from num2words import num2words
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

# setup
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# paths
input_path = "../data/reviews_raw.jsonl"
output_path = "../data/reviews_clean.jsonl"

# cleaning functions
def clean_text(text):
    if not text:
        return None

    # lowercase
    text = text.lower()

    # convert numbers to words
    text = re.sub(r'\d+', lambda x: num2words(int(x.group())), text)

    # remove emojis & special characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)

    # remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # tokenize
    tokens = nltk.word_tokenize(text)

    # remove stopwords + lemmatize
    cleaned_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words
    ]

    return " ".join(cleaned_tokens)


# process file
seen_ids = set()

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8") as outfile:

    for line in infile:
        review = json.loads(line)

        # remove duplicates
        review_id = review.get("reviewId")
        if review_id in seen_ids:
            continue
        seen_ids.add(review_id)

        content = review.get("content")

        # remove empty
        if not content or content.strip() == "":
            continue

        # clean text
        cleaned = clean_text(content)

        # remove extremely short reviews
        if not cleaned or len(cleaned.split()) < 3:
            continue

        # replace content with cleaned version
        review["content"] = cleaned

        # optionally remove original content (or keep both)
        # del review["content"]

        outfile.write(json.dumps(review, ensure_ascii=False) + "\n")

print("✅ Cleaning complete. Output saved to reviews_clean.jsonl")