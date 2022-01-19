import time

import pandas as pd
import streamlit as st
from envyaml import EnvYAML


def print_news(news_row):
    st.subheader(news_row["title"])
    st.write(f'{news_row["date"]}, {news_row["source"]}', unsafe_allow_html=True)
    if news_row["text"] is not None:
        if len(news_row["text"]) > 900:
            short_text = news_row["text"][:300]
        else:
            short_text = news_row["text"][:len(news_row["text"])//3]
        st.markdown(short_text + "...")
    st.markdown(f'<span class="blue">[Подробнее]({news_row["url"]})</span>', unsafe_allow_html=True)


def news_to_placeholder(archive_df, placeholder_item):
    with placeholder_item:
        with st.container():
            news = archive_df.sample(n=5)
            for index, row in news.iterrows():
                print_news(row)


def load_page():
    placeholder = st.empty()
    start_button = st.empty()

    config = EnvYAML("config_local.yaml")
    archive_path = config["data"]["archive"]
    archive = pd.read_parquet(archive_path)

    if start_button.button("Start", key="start"):
        start_button.empty()
        if st.button("Stop", key="stop"):
            pass
        while True:
            news_to_placeholder(archive, placeholder)
            time.sleep(10)
