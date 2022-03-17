import re

import streamlit as st

from util.data_preprocessing import filter_chunks
from util.otp_connector import get_filtered_articles, get_unique_values
from util.util import source_filter


def init_session_state(path):
    """
    initiate session state for news feed variables
    :param path: path to the archive
    """
    if "feed_regions" not in st.session_state:
        st.session_state["feed_regions"] = []
    if "feed_types" not in st.session_state:
        st.session_state["feed_types"] = []
    if "feed_sources" not in st.session_state:
        st.session_state["feed_sources"] = []
    if "feed_kw" not in st.session_state:
        st.session_state["feed_kw"] = ""
    if "feed_sources_list" not in st.session_state:
        st.session_state["feed_sources_list"] = sorted(get_unique_values(path, "source")["source"].values)
    if "feed_sources_types_list" not in st.session_state:
        st.session_state["feed_sources_types_list"] = ["СМИ", "Сайты ведомств и оперативных служб"]
    if "feed_region_list" not in st.session_state:
        st.session_state["feed_region_list"] = sorted(get_unique_values(path, "source_region")["source_region"].values)


def filter_params_form(ru_sw_file, mystem_model):
    """
    build streamlit form for the feed filter
    :param ru_sw_file: path to russian stopwords file
    :param mystem_model: MyStem model
    :return: chosen regions, source types and names, keywords and NE
    """
    st.subheader('Параметры фильтрации статей в ленте')
    sources_list = st.session_state["feed_sources_list"]
    source_types_list = st.session_state["feed_sources_types_list"]
    region_list = st.session_state["feed_region_list"]
    sources, source_types, regions = source_filter(sources_list, source_types_list, region_list,
                                                   "feed_sources", "feed_types", "feed_regions")
    kw = st.text_input('Поиск по ключевым словам, организациям, местам и героям публикаций (введите через запятую)',
                       value=st.session_state["feed_kw"])
    kw = [kw.strip().lower() for kw in kw.split(",") if len(kw.strip()) > 0]
    kw = filter_chunks(mystem_model, kw, ru_sw_file)
    return regions, source_types, sources, kw


def print_news(news_row):
    """
    printing function
    :param news_row: news row to print
    """
    st.subheader(news_row["title"])
    st.write(f'{news_row["date"]}, {news_row["source"]}', unsafe_allow_html=True)
    if news_row["text"] is not None:
        long_text = re.sub(r"[\n\r]+", " ", news_row["text"]).strip()
        if len(long_text) > 900:
            short_text = long_text[:300]
        else:
            short_text = long_text[:len(long_text) // 3]
        st.markdown(short_text + "...")
    st.markdown(f'<span class="blue">[Подробнее]({news_row["url"]})</span>', unsafe_allow_html=True)


def load_page(data_path, ru_sw_file, mystem_model):
    """
    load news feed page
    :param data_path: path to the archive
    :param ru_sw_file: path to russian stopwords file
    :param mystem_model: MyStem model
    """
    init_session_state(data_path)

    st.markdown("[Предложить источник](https://forms.yandex.ru/cloud/6231dd6bf0984d4d30ed61b9/)"
                " &nbsp; &nbsp; &nbsp; &nbsp; "
                "[Форма обратной связи](https://forms.yandex.ru/cloud/6231dbd47ffcaf612c42870e/)")
    st.title("Лента новостей")

    with st.form("feed_params_form"):
        regions, source_types, sources, kw = filter_params_form(ru_sw_file, mystem_model)
        feed_params_button = st.form_submit_button("Обновить ленту")
    if feed_params_button:
        st.session_state["feed_regions"] = regions
        st.session_state["feed_types"] = source_types
        st.session_state["feed_sources"] = sources
        st.session_state["feed_kw"] = ", ".join(kw)
    filtered_df = get_filtered_articles(data_path,
                                        sources=sources,
                                        source_types=source_types,
                                        regions=regions,
                                        kw_ne=kw,
                                        n=10)
    for index, row in filtered_df.iterrows():
        print_news(row)
