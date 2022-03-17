import streamlit as st


def set_style_conf():
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
