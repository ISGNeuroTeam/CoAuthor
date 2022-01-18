import time

import pandas as pd
import streamlit as st
from envyaml import EnvYAML


def print_news(news_row):
    with placeholder:
        with st.container():
            st.subheader(news_row['title'])
            st.write(f"{news_row['date']} <span class='red bold'>{news_row['source']}</span>", unsafe_allow_html=True)
            if news_row['text'] is not None:
                st.markdown(news_row['text'])
            st.markdown(f"<span class='blue'>[Подробнее]({news_row['url']})</span>", unsafe_allow_html=True)


placeholder = st.empty()
start_button = st.empty()

config = EnvYAML("config_local.yaml")
archive_path = config["data"]["archive"]
archive = pd.read_parquet(archive_path)


if start_button.button('Start',key='start'):
    start_button.empty()
    if st.button('Stop',key='stop'):
        pass
    while True:
        news = archive.sample(n=5)
        for index, row in news.iterrows():
            print_news(row)
        time.sleep(10)

