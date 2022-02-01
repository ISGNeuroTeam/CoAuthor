import streamlit as st

import context_gen

st.set_page_config(
    page_title="СоАвтор",
    layout="wide")

st.sidebar.title("Лента новостей")
st.sidebar.header("Здесь будет лента новостей")

page = st.selectbox("", ["Бекграунд", "Архив", "Аналитика"])
if page == "Бекграунд":
    context_gen.load_page()
elif page == "Архив":
    st.header("Загружается страница архива")
elif page == "Аналитика":
    st.header("Загружается страница аналитики")
