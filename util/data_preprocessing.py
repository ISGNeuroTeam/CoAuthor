from nltk import word_tokenize, pos_tag, RegexpParser
# from pymystem3 import Mystem

# m = Mystem(mystem_bin="/opt/otp/DataJournalismApp/models/mystem")


def lemmatize(mystem_model, sent):
    return [mystem_model.lemmatize(token) for token in sent]


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
        out_chunks.append(
            " ".join([lemma.translate(str.maketrans('', '', pattern_punct)).strip() for lemma in chunk if
                      lemma not in stopwords]).strip().lower()
        )
    return list(filter(lambda ch: len(ch) > 3, out_chunks))


def collect_np(text, ru_sw_file, mystem_model):
    text = text.lower()
    tokens = word_tokenize(text)
    return filter_chunks(mystem_model, tokens_to_chunks(tokens), ru_sw_file)
