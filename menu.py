import streamlit as st

import context_gen
import news_feed

st.set_page_config(
    page_title="СоАвтор",
    layout="wide")

# change sidebar width
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 500px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# output news feed to the sidebar
with st.sidebar:
    news_feed.load_page()

# load context page
context_gen.load_page()

# page = st.selectbox("", ["Бекграунд", "Архив", "Аналитика"])
# if page == "Бекграунд":
#     context_gen.load_page()
# elif page == "Архив":
#     st.header("Загружается страница архива")
# elif page == "Аналитика":
#     st.header("Загружается страница аналитики")
