import pandas as pd


def unite_kw_ne(input_kw: list, input_ne: list):
    return set(input_kw) | set(input_ne)


def get_sim_texts(archive_df: pd.DataFrame, input_kwne_total_score: dict, ref_num: int):
    archive_df["kwne_mean_score"] = archive_df["kwne_total_score"].apply(lambda kw_score_dict: dict(
        [(item[0], (item[1] + input_kwne_total_score[item[0]]) / 2) for item in kw_score_dict.items()]
    ))
    archive_df["total_score"] = 0.1 * archive_df["kwne_mean_score"] + 0.9 * archive_df["embedding_score"]
    return archive_df.sort_values("total_score", ascending=False)[:ref_num]
