import streamlit as st
from envyaml import EnvYAML
from pymystem3 import Mystem

import context_gen
import news_feed
from app_conf.authentication import info_form, is_authenticated, clean_blocks, authentication_page
from app_conf.style_config import set_style_conf


def main(config_file):
    bert_embedding_path = config_file["models"]["embedding"]
    ru_sw_file = config_file["data"]["ru_stopwords"]
    ref_num_default = int(config_file["params"]["reference_number"])
    sent_num_default = int(config_file["params"]["sentence_number"])
    data_path = config_file["connection"]["data_path"]
    otl_text_features = bool(config_file["params"]["otl_text_features"])
    read_mystem_local = bool(config_file["models"]["read_mystem_local"])
    mystem_path = config_file["models"]["local_mystem_path"]

    if read_mystem_local:
        mystem_model = Mystem(mystem_bin=mystem_path)
    else:
        mystem_model = Mystem()

    # output news feed to the sidebar
    with st.sidebar:
        news_feed.load_page(data_path, ru_sw_file, mystem_model)

    # load context page
    context_gen.load_page(bert_embedding_path, ru_sw_file, ref_num_default, sent_num_default, data_path,
                          otl_text_features, mystem_model)


set_style_conf()

config = EnvYAML("config_local.yaml")
login_list_path = config["authentication"]["login_list_path"]
login_list = open(login_list_path, "r").read().split("\n")

login_block, info_block, video_block = authentication_page()
if is_authenticated(st.session_state["login"], login_list):
    clean_blocks([login_block, info_block, video_block])
    main(config)
elif st.session_state["login"]:
    info_form(info_block, info="Такая почта не зарегистрирована")
