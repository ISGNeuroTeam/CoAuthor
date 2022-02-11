import streamlit as st
from envyaml import EnvYAML

from util.data_preprocessing import filter_chunks
from util.otp_connector import get_filtered_articles, get_unique_values


def filter_params_form(path, ru_sw_file):
    st.subheader('Параметры фильтрации статей в ленте')
    sources_list = get_unique_values(path, "source")["source"].values
    # kw_list = get_unique_values(path, "kw_ne")["kw_ne"].values
    sources = st.multiselect('Выберите источник(и)', sources_list)
    # kw = st.multiselect('Задайте ключевые слова или названия', kw_list)
    kw = st.text_input('Задайте ключевые слова или названия через запятую')
    kw = [kw.strip().lower() for kw in kw.split(",") if len(kw.strip()) > 0]
    kw = filter_chunks(kw, ru_sw_file)
    return sources, kw


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
    st.title("Лента новостей")

    config = EnvYAML("config_local.yaml")
    data_path = config["connection"]["data_path"]
    ru_sw_file = config["data"]["ru_stopwords"]
    # TODO: add form
    with st.form("params_form"):
        sources, kw = filter_params_form(data_path, ru_sw_file)
        st.form_submit_button("Обновить ленту")
    filtered_df = get_filtered_articles(data_path, sources=sources, kw_ne=kw, n=15)
    for index, row in filtered_df.iterrows():
        print_news(row)
