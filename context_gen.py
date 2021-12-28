import time

import pandas as pd
import streamlit as st
from envyaml import EnvYAML

from util import text_embedding, abstractive_summarization, extractive_summarization, grammar_check

config = EnvYAML("config_local.yaml")
rubert_path = config["models"]["rubert_tiny"]
rut5_ru_sum_path = config["models"]["rut5_sum"]
archive_path = config["data"]["archive"]
ref_num_default = int(config["params"]["reference_number"])
sent_num_default = int(config["params"]["sentence_number"])
sim_threshold_default = float(config["params"]["similarity_threshold"])

archive_texts = pd.read_parquet(archive_path)
grammar_tool = grammar_check.download_tool()


def load_page():
    st.title('Генерация бекграунда')
    # col1, col2 = st.columns([1, 3])
    button_name = "Сформировать бекграунд статьи"
    input_text = st.text_area('Начните набирать текст в поле. '
                              'Когда текст готов, задайте настройки и нажмите  "%s"' % button_name,
                              height=700)
    input_vec = text_embedding.embed_bert_cls(input_text, rubert_path, rubert_path)

    grammar_button = st.button("Проверить правописание")
    grammar_container = st.container()

    if grammar_button:
        matches = grammar_check.find_mistakes(input_text, grammar_tool)
        with grammar_container:
            for i, match in enumerate(matches):
                context, error_flag, message = grammar_check.print_match(match)
                st.write(str(i + 1) + ": " + message)
                st.text(context + error_flag)
        if st.button("Спрятать проверку текста"):
            del grammar_container

    with st.expander("Параметры для генерации бекграунда", expanded=False):
        with st.form("params_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Параметры фильтрации документов')

                sources_list = sorted(archive_texts["source"].unique())
                sources = st.multiselect('Выберите источник', sources_list)
                if len(sources) > 0:
                    filtered_df = archive_texts[archive_texts["source"].apply(lambda s: s in sources)]
                else:
                    filtered_df = archive_texts.copy()

                dates = st.date_input("Задайте период поиска", value=[])
                if len(dates) > 0:
                    start, end = dates
                    start = time.mktime(start.timetuple())
                    end = time.mktime(end.timetuple())
                    filtered_df = archive_texts[(archive_texts["_time"] >= start) & (archive_texts["_time"] <= end)]

            with col2:
                st.subheader('Настройки генерации бекграунда')

                summ_type = st.selectbox('Выберите способ',
                                         ["Экстрактивная суммаризация", "Абстрактивная суммаризация"])

                ref_num = st.slider("Выберите максимальное число документов для генерации бекграунда",
                                    min_value=1,
                                    max_value=10,
                                    value=ref_num_default,
                                    step=1)

                sim_threshold = st.slider("Выберите степень похожести найденных документов на ваш текст",
                                          min_value=0.0,
                                          max_value=1.0,
                                          value=0.8,
                                          step=0.1)

                sent_num = st.slider("Выберите число предложений, которое нужно сформировать",
                                     min_value=1,
                                     max_value=5,
                                     value=sent_num_default,
                                     step=1)
                # TODO: add check for input type (does streamlit has one??)

            st.form_submit_button("Применить настройки")

    gen_button = st.button(button_name)

    if gen_button:
        if len(filtered_df) == 0:
            st.write("Я не нашёл подходящие под параметры фильтрации тексты. Попробуйте поменять настройки.")
        elif len(filtered_df) > 0:
            sim_texts_df = text_embedding.find_sim_texts(filtered_df.dropna(), input_vec, ref_num, sim_threshold)
            if len(sim_texts_df) == 0:
                st.write("Я не нашёл подходящие под параметры фильтрации тексты. Попробуйте поменять настройки.")
            sim_texts = sim_texts_df[["clean_text", "text"]].values.tolist()
            art_inds = sim_texts_df.index
            urls = sim_texts_df["url"].values
            if summ_type == "Абстрактивная суммаризация":
                context = abstractive_summarization.sum_text(sim_texts, rut5_ru_sum_path)
                for i, doc in enumerate(context):
                    st.write(str(i + 1))
                    st.write(doc)
                    st.write("\n\n")
            else:
                context = extractive_summarization.lexrank_sum(sim_texts, sent_num=sent_num)
                for i, doc in enumerate(context):
                    st.markdown("[%s](%s)" % (art_inds[i], urls[i]))
                    output = ""
                    for sentence in doc:
                        output += sentence
                        output += " "
                    st.write(output)
