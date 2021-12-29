import numpy as np
import pandas as pd

from util.data_preprocessing import lemmatize


def unite_kw_ne(input_kw: list, input_ne: list):
    kw = [token.replace("%", " ") for token in input_kw]
    ne = lemmatize(input_ne)
    return set(kw) | set(ne)


def get_kwne_sim(input_kw_ne: set, archive_df: pd.DataFrame, sim_texts: list):
    sim_ind = [x[0] for x in sim_texts]
    sim_score = [x[1] for x in sim_texts]
    sim_kw_ne = [set(kw) for kw in archive_df.loc[sim_ind, "kw_ne"].values]
    common_kw_ne = np.array([len(kw & input_kw_ne) / len(kw | input_kw_ne) + 1.0 for kw in sim_kw_ne])
    similarities = sorted(list(zip(sim_ind, np.multiply(sim_score, common_kw_ne))), key=lambda x: x[1], reverse=True)
    return similarities
