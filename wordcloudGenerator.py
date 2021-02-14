from sentimentAnalyzer import *
import re
import matplotlib.pyplot as plt
import nltk
from textblob_de import TextBlobDE as TextBlob
from textblob_de.lemmatizers import PatternParserLemmatizer
from wordcloud import WordCloud
from nltk.corpus import stopwords
from string import punctuation, digits
from HanTa import HanoverTagger as ht

with open(r"C:\Texte\UNI\Master WiInfo\Seminararbeit UM\youtube\comments"
          r"\der_große_e_sharing_vergleich_in_berlin_tier_circ_voi_test_anleitung_review_escooter_ger.txt", encoding="utf-8") as f:
    parsed_json = f.readlines()

ger_stopwords = stopwords.words("german")
scooter_stopwords = ["roller", "scooter", "stadt", "fahren",
                     "tier", "lime", "fahrt", "städte", "gut",
                     "schlecht", "vergleich", "video", "besten",
                     "minuten", "sekunden", "circ", "voi", "bird"]  # additional words to be removed
all_stopwords = ger_stopwords + scooter_stopwords

lemmatizer = PatternParserLemmatizer()
search_tags = ["NN", "ADJD", "ADJA"]  # "VB"
tagger = ht.HanoverTagger("morphmodel_ger.pgz")


def word_tokenizer(data):
    data_string = " ".join(data)  # join list of strings together to one single string so tokenize works properly

    remove_punc = str.maketrans("", "", punctuation)
    no_punc = data_string.translate(remove_punc)

    remove_digits = str.maketrans("", "", digits)
    no_digits = no_punc.translate(remove_digits)

    blob = TextBlob(no_digits)
    words_tokenized = blob.tokens

    return words_tokenized


def filter_by_pos(data, pos_tags):
    stops_removed = [word for word in data
                     if tagger.analyze(word)[0].lower() and word.lower() not in all_stopwords]  # remove stop words
    pos_tags_han = tagger.tag_sent(stops_removed)  # hanover tagger requires list of str for tagging
    print(stops_removed)
    # print(blob.tags)
    filtered_tags = [token for token in pos_tags_han if token[2] in pos_tags]
    # print(pos_tags_han)
    # print(pos_tags)
    filtered_tokens = [tokens[0] for tokens in filtered_tags]  # filter out the pos tags, only tokens remain as list of str

    return filtered_tokens


def generate_wc(tokens):
    wordC = WordCloud(width=800, height=800, background_color="white", min_font_size=10).generate(" ".join(tokens))
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordC)
    plt.axis("off")
    plt.tight_layout(pad=0)
    return plt

cleaned_data = clean_json(parsed_json)
cleaned_de = allocate_lang(cleaned_data, lang="de")
# print(all_stopwords)

tokenized_words = word_tokenizer(cleaned_de)
# print(tokenized_words)

filtered_words = filter_by_pos(tokenized_words, search_tags)
# print(filtered_words)

wc = generate_wc(filtered_words)
wc.show()

# fdist = nltk.FreqDist(filtered_words)
# for word, frequency in fdist.most_common(30):
#      print("{};{}".format(word, frequency))
# fdist.plot(30)
