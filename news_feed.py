import re

import streamlit as st

from util.data_preprocessing import filter_chunks
from util.otp_connector import get_filtered_articles, get_unique_values
from util.util import check_multiselect_default


def filter_params_form(path, ru_sw_file, mystem_model):
    st.subheader('Параметры фильтрации статей в ленте')
    sources_list = sorted(get_unique_values(path, "source")["source"].values)
    source_types_list = ["СМИ", "Сайты ведомств и оперативных служб"]
    region_list = sorted(get_unique_values(path, "source_region")["source_region"].values)
    if "" in region_list:
        region_list.remove("")
    if "Россия" in region_list:
        region_list.remove("Россия")
    region_list.append("Федеральные СМИ")
    sources_default = check_multiselect_default("feed_sources", sources_list)
    sources = st.multiselect('Выберите источники по названию',
                             sources_list,
                             default=sources_default)
    sources_types_default = check_multiselect_default("feed_types", source_types_list)
    source_types = st.multiselect('Или по типу источника...',
                                  source_types_list,
                                  default=sources_types_default)
    regions_default = check_multiselect_default("feed_regions", region_list)
    regions = st.multiselect('...и региону',
                             region_list,
                             default=regions_default)
    kw = st.text_input('Поиск по ключевым словам, организациям, местам и героям публикаций (введите через запятую)',
                       value=st.session_state["feed_kw"])
    kw = [kw.strip().lower() for kw in kw.split(",") if len(kw.strip()) > 0]
    kw = filter_chunks(mystem_model, kw, ru_sw_file)
    return regions, source_types, sources, kw


def print_news(news_row):
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
    if "feed_regions" not in st.session_state:
        st.session_state["feed_regions"] = []
    if "feed_types" not in st.session_state:
        st.session_state["feed_types"] = []
    if "feed_sources" not in st.session_state:
        st.session_state["feed_sources"] = []
    if "feed_kw" not in st.session_state:
        st.session_state["feed_kw"] = ""

    st.markdown("[Предложить источник](https://forms.yandex.ru/cloud/6231dd6bf0984d4d30ed61b9/) &nbsp; &nbsp; &nbsp; &nbsp; [Форма обратной связи](https://forms.yandex.ru/cloud/6231dbd47ffcaf612c42870e/)")
    st.title("Лента новостей")

    with st.form("feed_params_form"):
        regions, source_types, sources, kw = filter_params_form(data_path, ru_sw_file, mystem_model)
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
