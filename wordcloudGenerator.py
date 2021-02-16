from textblob_de import TextBlobDE as TextBlob
from wordcloud import WordCloud
from nltk.corpus import stopwords
from string import punctuation, digits
from HanTa import HanoverTagger as ht
from sentimentAnalyzer import allocate_lang, clean_file
import matplotlib.pyplot as plt


class StopWordsRemover:
    """ This class contains two methods which a) sentence tokenize and remove punctuation and digits
    b) filter the text by stopwords, optional additional words which can be inserted by list
    and by part-of-speech tags which have to be specified an inserted as list  """

    @staticmethod
    def word_tokenizer(data):
        data_string = " ".join(data)  # join list of strings together to one single string so tokenize works properly

        remove_punc = str.maketrans("", "", punctuation)
        no_punc = data_string.translate(remove_punc)

        remove_digits = str.maketrans("", "", digits)
        no_digits = no_punc.translate(remove_digits)

        blob = TextBlob(no_digits)
        words_tokenized = blob.tokens

        return words_tokenized

    @staticmethod
    def filter_by_pos(data, pos_tags, custom_stopwords=""):
        ger_stopwords = stopwords.words("german")
        all_stopwords = ger_stopwords + custom_stopwords
        tagger = ht.HanoverTagger("morphmodel_ger.pgz")

        stops_removed = [word for word in data
                         if tagger.analyze(word)[
                             0].lower() and word.lower() not in all_stopwords]  # remove stop words
        pos_tags_han = tagger.tag_sent(stops_removed)  # hanover tagger requires list of str for tagging
        filtered_tags = [token for token in pos_tags_han if token[2] in pos_tags]

        # filter out the pos tags, only tokens remain as list of str
        filtered_tokens = [tokens[0] for tokens in filtered_tags]

        return filtered_tokens


def generate_wc(tokens):
    """ This method generates a wordcloud and returns the figure """
    wcloud = WordCloud(width=800, height=800, background_color="black", min_font_size=10).generate(" ".join(tokens))
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    return plt


def wordcloud_from_file(filepath, lang="de"):
    """ This method uses methods from other py files (sentimentAnalyzer) and from the StopWordsRemover class
    to create a wordcloud from a text file containing strings"""
    cleaned_data = clean_file(filepath)
    cleaned_data = allocate_lang(cleaned_data, lang)
    tokenized_words = StopWordsRemover.word_tokenizer(cleaned_data)
    filtered_words = StopWordsRemover.filter_by_pos(tokenized_words, search_tags, additional_stopwords)
    generate_wc(filtered_words).show()


# example, additional words that ought to be removed from text
additional_stopwords = ["roller", "scooter", "stadt", "fahren",
                        "tier", "lime", "fahrt", "städte", "gut",
                        "schlecht", "vergleich", "video", "besten",
                        "minuten", "sekunden", "circ", "voi", "bird", "km", "echt", "cool"]
# example, give out these pos tags
search_tags = ["NN", "ADJD", "ADJA"]

file_path = r""  # specify file path
wordcloud_from_file(file_path)
