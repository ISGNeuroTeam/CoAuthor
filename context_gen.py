import numpy as np
import streamlit as st
from envyaml import EnvYAML

from util import extractive_summarization, grammar_check, text_embedding, kwne_similarity
from util.otp_connector import get_text_features_eep, get_unique_source_topics, get_filtered_articles

config = EnvYAML("config_local.yaml")
bert_embedding_path = config["models"]["embedding"]
rut5_ru_sum_path = config["models"]["rut5_sum"]
archive_path = config["data"]["archive"]
ru_sw_file = config["data"]["ru_stopwords"]
ref_num_default = int(config["params"]["reference_number"])
sent_num_default = int(config["params"]["sentence_number"])
data_path = config["connection"]["data_path"]

grammar_tool = grammar_check.download_tool()


def get_text_features(input_text):
    input_df = get_text_features_eep(input_text.replace("\n", " ").replace("\r", " ").replace('"', ''))
    input_kw_ne = set(input_df["kw_ne"].values[0].split("; "))
    input_vec = np.array(input_df["embedding"].values[0].split("; "))
    return input_kw_ne, input_vec


def check_grammar_on_click(input_text: str, grammar_container: st.container):
    matches = grammar_check.find_mistakes(input_text, grammar_tool)
    with grammar_container:
        for i, match in enumerate(matches):
            context, error_flag, message = grammar_check.print_match(match)
            st.write(str(i + 1) + ": " + message)
            st.text(context + error_flag)
    if st.button("Спрятать проверку текста"):
        del grammar_container


def filter_params_form(path):
    st.subheader('Параметры фильтрации документов')
    sources_list = get_unique_source_topics(path, "source")["source"].values
    sources = st.multiselect('Выберите источник', sources_list)
    dates = st.date_input("Задайте период поиска", value=[])
    return sources, dates


def context_params_form():
    st.subheader('Настройки генерации бекграунда')

    ref_num = st.slider("Выберите максимальное число документов для генерации бекграунда",
                        min_value=1,
                        max_value=10,
                        value=ref_num_default,
                        step=1)

    sent_num = st.slider("Выберите число предложений, которое нужно сформировать",
                         min_value=1,
                         max_value=5,
                         value=sent_num_default,
                         step=1)
    return ref_num, sent_num


def generate_context(path, dates, sources, input_vec, input_kw_ne, ref_num, sent_num):
    filtered_df = get_filtered_articles(path, dates, sources)
    cos_sim_ind_score = text_embedding.find_sim_texts(filtered_df.dropna(),
                                                      input_vec,
                                                      ref_num,
                                                      full_output=True)
    filtered_df = filtered_df.set_index("art_ind")
    sim_ind_score = kwne_similarity.get_kwne_sim(input_kw_ne, filtered_df, cos_sim_ind_score)
    sim_ind = [x[0] for x in sim_ind_score][:ref_num]
    sim_texts_df = filtered_df.loc[sim_ind]

    if len(sim_texts_df) == 0:
        st.write("Я не нашёл подходящие под параметры фильтрации тексты. Попробуйте поменять настройки.")

    sim_texts = sim_texts_df[["clean_text", "text"]].values.tolist()
    art_inds = sim_texts_df.index
    urls = sim_texts_df["url"].values

    context = extractive_summarization.lexrank_sum(sim_texts, sent_num=sent_num)
    for i, doc in enumerate(context):
        st.markdown("[%s](%s)" % (art_inds[i], urls[i]))
        output = ""
        for sentence in doc:
            output += sentence
            output += " "
        st.write(output)


def load_page():
    st.title('Генерация бекграунда')
    button_name = "Сформировать бекграунд статьи"
    input_text = st.text_area('Начните набирать текст в поле. '
                              'Когда текст готов, задайте настройки и нажмите  "%s"' % button_name,
                              height=700)
    input_kw_ne, input_vec = get_text_features(input_text)

    grammar_button = st.button("Проверить правописание")
    grammar_container = st.container()

    if grammar_button:
        check_grammar_on_click(input_text, grammar_container)

    with st.expander("Параметры для генерации бекграунда", expanded=False):
        with st.form("params_form"):
            col1, col2 = st.columns(2)
            with col1:
                sources, dates = filter_params_form(data_path)
            with col2:
                ref_num, sent_num = context_params_form()
            st.form_submit_button("Применить настройки")

    gen_button = st.button(button_name)

    if gen_button:
        generate_context(data_path, dates, sources, input_vec, input_kw_ne, ref_num, sent_num)
