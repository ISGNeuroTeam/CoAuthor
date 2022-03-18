import numpy as np
import pandas as pd

from text_util.data_preprocessing import lemmatize


def unite_kw_ne(input_kw: list, input_ne: list, mystem_model):
    kw = [token.replace("%", " ") for token in input_kw]
    ne = [" ".join(item).strip() for item in lemmatize(mystem_model, input_ne)]
    return set(kw) | set(ne)


def get_kwne_sim(archive_df: pd.DataFrame, sim_texts: list):
    sim_ind = [x[0] for x in sim_texts]
    sim_score = [x[1] for x in sim_texts]
    sim_kw_ne = archive_df.loc[sim_ind, "kw_sum_score"].values
    common_kw_ne = np.array([kw_sum_score + 1.0 for kw_sum_score in sim_kw_ne])
    similarities = sorted(list(zip(sim_ind, np.multiply(sim_score, common_kw_ne))), key=lambda x: x[1], reverse=True)
    return similarities
