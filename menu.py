import pandas as pd
import streamlit as st
from envyaml import EnvYAML

import context_gen

st.set_page_config(
    page_title="Помощник журналиста",
    layout="wide")

config = EnvYAML("config_local.yaml")
archive_path = config["data"]["archive"]
archive = pd.read_parquet(archive_path)

page = st.selectbox("", ["Бекграунд", "Архив", "Аналитика"])
if page == "Бекграунд":
    context_gen.load_page()
elif page == "Архив":
    st.header("Загружается страница архива")
elif page == "Аналитика":
    st.header("Загружается страница аналитики")


# while True:
#     if time.time() % 30 == 0:
#         st.sidebar.title("Лента новостей")
#         news = archive.sample(n=5)
#         st.write(news)
#         # for news_row in news.values:
#         #     st.subheader(news_row['title'])
#         #     st.write(f"{news_row['date']} <span class='red bold'>{news_row['source']}</span>", unsafe_allow_html=True)
#         #     if news_row['text'] is not None:
#         #         st.markdown(news_row['text'])
#         #     st.markdown(f"<span class='blue'>[Подробнее]({news_row['url']})</span>", unsafe_allow_html=True)
