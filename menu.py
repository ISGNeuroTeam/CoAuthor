import streamlit as st

import archive
import context_gen
import news_feed

st.set_page_config(
    page_title="Помощник журналиста",
    page_icon=":memo:",
    layout="wide",
    initial_sidebar_state="expanded")


def clean_cache():
    # Delete all the items in Session state
    for key in st.session_state.keys():
        del st.session_state[key]


page = st.sidebar.radio("Меню приложения", ["Лента новостей", "Бекграунд", "Архив", "Аналитика"])

if page == "Бекграунд":
    # clean_cache()
    for key in st.session_state.keys():
        st.write(key, st.session_state[key])
    context_gen.load_page()
elif page == "Архив":
    archive.load_page()
elif page == "Аналитика":
    st.header("Загружается страница аналитики")
elif page == "Лента новостей":
    for key in st.session_state.keys():
        st.write(key, st.session_state[key])
    # clean_cache()
    news_feed.load_page()
