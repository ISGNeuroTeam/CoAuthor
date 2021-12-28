import re

import pymorphy2
from razdel import sentenize, tokenize

morph = pymorphy2.MorphAnalyzer()


def remove_stop_words_punct(sent, stopwords):
    ru_sw = open(stopwords, "r+").read().split("\n")
    # TODO: add file not found error
    pattern_punct = '[\.!@"“’«»#$%&\'()*+,—/:;<=>?^_`{|}~\[\]]'
    return [token for token in sent if token not in ru_sw and not token.isdigit() and token not in pattern_punct]


def lemmatize(sent):
    return [(morph.parse(token)[0]).normal_form for token in sent]


def remove_citation(text):
    return text.replace('""', "").replace('"', "").replace("“", "").replace("”", "").replace("«", "").replace("»", "")


def text_preprocessing(text, ru_sw_file):
    text = text.replace('\xa0', ' ')
    pattern_url = 'http[s]?://\S+|www\.\S+'
    pattern_tags = '<.*?>'

    clean_text = re.sub(pattern_tags, "", re.sub(pattern_url, "", text))
    sentences = [t.text for t in sentenize(clean_text)]
    tokens = [[t.text for t in tokenize(sent)] for sent in sentences]
    tokens = [lemmatize(sent) for sent in tokens]
    tokens = [remove_stop_words_punct(sent, ru_sw_file) for sent in tokens]
    return tokens
