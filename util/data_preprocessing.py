import re

import nltk
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


def flatten_list(input_list):
    out = []
    for nested_list in input_list:
        out.extend(nested_list)
    return out


def get_pos(tokens):
    return nltk.pos_tag(tokens, lang='rus')


def collect_np(lemma_pos_list: list, adjective_tag=frozenset(["ADJ"]), noun_tag=frozenset(["NOUN", "PROPN"])):
    """
    Collect only noun phrases from text: [ADJ*(NOUN|PROPN)+]
    :param noun_tag: code for the noun tag, NN by default (the Penn Treebank Project)
    :param adjective_tag: code for the adjective tag, JJ by default (the Penn Treebank Project)
    :param lemma_pos_list: list of pairs [(lemma, pos)]
    :return: list of noun phrases from text
    """
    prev_pos = "START"
    noun_phrases = []
    phrase = []
    for w in lemma_pos_list:
        pos = w[1]
        word = w[0]
        if pos in adjective_tag and len(word) > 1:
            if prev_pos in adjective_tag or len(phrase) == 0:
                phrase.append(word)
            else:
                noun_phrases.append("%".join(phrase))
                phrase = [word]
        elif pos in noun_tag and len(word) > 1:
            phrase.append(word)
        else:
            if len(phrase) > 0:
                noun_phrases.append("%".join(phrase))
                phrase = []
        prev_pos = pos
    return noun_phrases
