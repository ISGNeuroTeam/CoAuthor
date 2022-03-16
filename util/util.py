import streamlit as st


def check_multiselect_default(session_state_name, options):
    default_value = st.session_state[session_state_name]
    if set(default_value) | set(options) != set(options):
        default_value = set(default_value) & set(options)
    return default_value
