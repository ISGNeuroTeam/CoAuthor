from collections import Counter

import numpy as np
import pandas as pd

from text_util.data_preprocessing import lemmatize


def unite_kw_ne(input_kw: list, input_ne: list, mystem_model):
    kw = [token.replace("%", " ") for token in input_kw]
    ne = [" ".join(item).strip() for item in lemmatize(mystem_model, input_ne)]
    return set(kw) | set(ne)


def get_kwne_sim(input_kw_ne: set, archive_df: pd.DataFrame, sim_texts: list):
    sim_ind = [x[0] for x in sim_texts]
    sim_score = [x[1] for x in sim_texts]
    # sim_kw_ne = [set(kw.split("; ")) for kw in archive_df.loc[sim_ind, "kw_ne"].values]
    sim_kw_ne = [np.array(kw.split("; ")) for kw in archive_df.loc[sim_ind, "kw_ne"].values]
    all_words = []
    for kw in sim_kw_ne:
        all_words.extend(list(kw))
    all_words_count = Counter(all_words)
    common_kw_ne = np.array(
        [np.sum([1 / all_words_count[kw] for kw in kw_list if kw in input_kw_ne]) + 1.0 for kw_list in sim_kw_ne])
    # common_kw_ne = np.array([len(kw & input_kw_ne) / len(kw | input_kw_ne) + 1.0 for kw in sim_kw_ne])
    similarities = sorted(list(zip(sim_ind, np.multiply(sim_score, common_kw_ne))), key=lambda x: x[1], reverse=True)
    # similarities = sorted(list(zip(sim_ind, sim_score)), key=lambda x: x[1], reverse=True)
    return similarities
