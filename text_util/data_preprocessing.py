import re

from nltk import word_tokenize, pos_tag, RegexpParser
from razdel import sentenize


def lemmatize(mystem_model, sent):
    return [mystem_model.lemmatize(token) for token in sent]


def remove_stop_words_punct(sent, ru_sw):
    pattern_punct = '[\.!@"“’«»#$%&\'()*+,—/:;<=>?^_`{|}~\[\]] [\n]'
    return [token.strip() for token in sent if
            token.strip() not in ru_sw and not token.strip().isdigit() and token.strip() not in pattern_punct]


# takes raw text, dict of stopwords and output clean and lemmatized text
def text_preprocessing(text, ru_sw, lemmatizer):
    text = text.replace('\xa0', ' ')
    pattern_url = 'http[s]?://\S+|www\.\S+'
    pattern_tags = '<.*?>'

    clean_text = re.sub(pattern_tags, "", re.sub(pattern_url, "", text))
    sentences = [t.text for t in sentenize(clean_text)]
    tokens = lemmatize(lemmatizer, sentences)
    tokens = [remove_stop_words_punct(sent, ru_sw) for sent in tokens]
    return [" ".join(sent) for sent in tokens]


def tokens_to_chunks(tokens):
    tagged = pos_tag(tokens, lang='rus')
    chunk_gram = r"""Chunk: {<A=.?>*<S>+}"""  # collect noun phrases with adjectives and nouns
    chunk_parser = RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(tagged)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        chunks.append(" ".join([leaf[0] for leaf in subtree.leaves()]))
    return chunks


def filter_chunks(mystem_model, chunks, ru_sw_file):
    pattern_punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»…“„—'
    stopwords = open(ru_sw_file, "r+").read().split("\n")
    # TODO: add file not found error
    chunks = [mystem_model.lemmatize(chunk) for chunk in chunks]
    out_chunks = []
    for chunk in chunks:
        new_chunk = [lemma.translate(str.maketrans('', '', pattern_punct)).strip() for lemma in chunk if
                     lemma not in stopwords]
        new_chunk = [lemma for lemma in new_chunk if len(lemma) > 0]
        if len(new_chunk) > 0:
            out_chunks.append(" ".join(new_chunk).strip().lower())
    return list(filter(lambda ch: len(ch) > 3, out_chunks))


def collect_np(text, ru_sw_file, mystem_model):
    text = text.lower()
    tokens = word_tokenize(text)
    return filter_chunks(mystem_model, tokens_to_chunks(tokens), ru_sw_file)
