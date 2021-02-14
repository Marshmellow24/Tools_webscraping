from langdetect import detect
from textblob_de import TextBlobDE as TextBlob
from textblob import TextBlob as TextBlobEN
import re
from langdetect import detect

with open(r"C:\Texte\UNI\Master WiInfo\Seminararbeit UM\youtube\comments"
          r"\e_scooter_zum_ausleihen_das_bieten_tier_circ_und_voi.txt", encoding="utf-8") as f:
    raw = f.readlines()


REMOVE_LINESEP = re.compile(r"\n", re.IGNORECASE)
# REMOVE_ID = re.compile(r"^.{11}$", re.IGNORECASE)
REMOVE_ASTERISKS = re.compile(r"^\*+", re.IGNORECASE)
REMOVE_INDEX = re.compile(r"^\d+$", re.IGNORECASE)
SLIM_SENTIMENT = re.compile(r"Sentiment\(polarity=|, subjectivity=\d.\d*\)")


# regex patterns for data cleaning of json parsed files


def clean_json(data):
    output = []
    for sentence in data:
        lineSep_removed = re.sub(REMOVE_LINESEP, "", sentence)
        # id_removed = re.sub(REMOVE_ID, "", lineSep_removed)
        ast_removed = re.sub(REMOVE_ASTERISKS, "", lineSep_removed)
        index_removed = re.sub(REMOVE_INDEX, "", ast_removed)

        if index_removed:  # only add non-empty strings to list
            output.append(index_removed)

    return output


# allocate sentences to lists according to their detected language


def allocate_lang(data, lang):
    cleaned_de = []
    cleaned_en = []
    cleaned_langs = (cleaned_de, cleaned_en)

    for clean_token in data:
        if detect(clean_token) != "de":
            cleaned_en.append(clean_token.strip())
        else:
            cleaned_de.append(clean_token.strip())

    if lang == "de":
        return cleaned_de
    elif lang == "en":
        return cleaned_en
    else:
        return cleaned_langs


# create list of tuples containing cleaned tokens and sentiment probabilities


def compute_sentiments(data):
    sentiments = []
    for token in data:
        blob = TextBlob(token)
        sentiment_value = re.sub(SLIM_SENTIMENT, "", str(blob.sentiment))
        sentiments.append((token, float(sentiment_value)))
    for token in data:
        blob = TextBlobEN(token)
        sentiment_value = re.sub(SLIM_SENTIMENT, "", str(blob.sentiment))
        sentiments.append((token, float(sentiment_value)))
    return sentiments


#print(clean_data(raw))
# print(allocate_lang(clean_data(raw), lang="de"))
# cleaned = clean_json(raw)
# languaged = allocate_lang(cleaned, lang="de")
#
# print(compute_sentiments(languaged))
# cleaned = clean_json(raw)
# languaged = allocate_lang(cleaned, lang="de")
# print(compute_sentiments(languaged))
