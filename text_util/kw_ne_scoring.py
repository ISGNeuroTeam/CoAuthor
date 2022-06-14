import string

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tf_idf_for_data(dataset, column_name):
    corpus = dataset[column_name].apply(lambda x: " ".join(["".join(kw.split(" ")) for kw in x])).values
    vectorizer = TfidfVectorizer()
    corpus_matrix = vectorizer.fit_transform(corpus)
    corpus_matrix = np.array(corpus_matrix.todense())

    token_to_ind = dict(zip(vectorizer.get_feature_names(), range(len(vectorizer.get_feature_names()))))
    return vectorizer, corpus_matrix, token_to_ind


def tf_idf_score(corpus_matrix, row, token_to_ind, column):
    temp_kw = ["".join(kw.split(" ")).translate(str.maketrans('', '', string.punctuation+"–")) for kw in row[column]]
    ids = [token_to_ind.get(kw, -1) for kw in temp_kw if kw]
    tfidf_scores = [corpus_matrix[row.name][ind] if ind != -1 else 0.0 for ind in ids]
    return dict(zip(row[column], tfidf_scores))


def compute_total_kw_score(kwne_tfidf_score, kw_textrank_score):
    total_score = dict()
    for kw in kwne_tfidf_score:
        if kw in kw_textrank_score:
            total_score[kw] = kwne_tfidf_score[kw] * kw_textrank_score[kw]
        else:
            total_score[kw] = kwne_tfidf_score[kw]
    return total_score

