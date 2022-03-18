import numpy as np
import streamlit as st
from transformers import AutoTokenizer, AutoModel

from app_util.otp_connector import get_text_features_eep, get_unique_values, get_filtered_articles_with_kw_score
from app_util.util import source_filter
from text_util import extractive_summarization, grammar_check, text_embedding, kwne_similarity, data_preprocessing, \
    ner_finder, textrank

grammar_tool = grammar_check.download_tool()


def init_session_state(sent_num_default, ref_num_default, path):
    if "context_regions" not in st.session_state:
        st.session_state["context_regions"] = []
    if "context_types" not in st.session_state:
        st.session_state["context_types"] = []
    if "context_sources" not in st.session_state:
        st.session_state["context_sources"] = []
    if "context_dates" not in st.session_state:
        st.session_state["context_dates"] = []
    if "sent_num" not in st.session_state:
        st.session_state["sent_num"] = sent_num_default
    if "ref_num" not in st.session_state:
        st.session_state["ref_num"] = ref_num_default
    if "context_output" not in st.session_state:
        st.session_state["context_output"] = []
    if "context_sources_list" not in st.session_state:
        st.session_state["context_sources_list"] = sorted(get_unique_values(path, "source")["source"].values)
    if "context_sources_types_list" not in st.session_state:
        st.session_state["context_sources_types_list"] = ["СМИ", "Сайты ведомств и оперативных служб"]
    if "context_region_list" not in st.session_state:
        st.session_state["context_region_list"] = sorted(get_unique_values(path, "source_region")["source_region"].values)


@st.experimental_memo
def get_text_features_otp(input_text):
    input_df = get_text_features_eep(input_text.replace("\n", " ").replace("\r", " ").replace('"', ''))
    input_kw_ne = set(input_df["kw_ne"].values[0].split("; "))
    input_vec = np.array(input_df["embedding"].values[0].split("; "))
    return input_kw_ne, input_vec


@st.experimental_memo
def get_text_features(input_text, ru_sw_file, _mystem_model, bert_embedding_path):
    input_noun_phrases = data_preprocessing.collect_np(input_text, ru_sw_file, _mystem_model)
    input_kw = textrank.text_rank(input_noun_phrases, 15)
    input_ne = data_preprocessing.filter_chunks(_mystem_model, ner_finder.finder(input_text), ru_sw_file)
    input_kw_ne = kwne_similarity.unite_kw_ne(input_kw, input_ne, _mystem_model)

    tokenizer = AutoTokenizer.from_pretrained(bert_embedding_path)
    model = AutoModel.from_pretrained(bert_embedding_path)
    # TODO: add file not found error
    input_vec = text_embedding.embed_labse(input_text, tokenizer, model)
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


def filter_params_form():
    st.subheader('Параметры фильтрации документов')
    sources_list = st.session_state["context_sources_list"]
    source_types_list = st.session_state["context_sources_types_list"]
    region_list = st.session_state["context_region_list"]
    sources, source_types, regions = source_filter(sources_list, source_types_list, region_list,
                                                   "context_sources", "context_types", "context_regions")
    dates = st.date_input("Задайте период поиска",
                          value=st.session_state["context_dates"])
    return regions, source_types, sources, dates


def context_params_form(input_kw_ne):
    if input_kw_ne is None:
        input_kw_ne = []
    st.subheader('Настройки генерации бекграунда')

    ref_num = st.slider("Выберите максимальное число документов для генерации бекграунда",
                        min_value=1,
                        max_value=10,
                        value=st.session_state["ref_num"],
                        step=1)

    sent_num = st.slider("Выберите число предложений, которое нужно сформировать",
                         min_value=1,
                         max_value=5,
                         value=st.session_state["sent_num"],
                         step=1)

    if len(input_kw_ne) > 0:
        kw_ne = st.multiselect("Выберите ключевые слова для более точного формирования бекграунда",
                               sorted(list(input_kw_ne)))
    else:
        kw_ne = []
    return ref_num, sent_num, kw_ne


@st.experimental_memo
def generate_context(path, dates, sources, source_types, regions, input_vec, input_kw_ne, ref_num, sent_num):
    stop_kw = "день, неделя, год, тасс, интерфакс, страна, число, январь, февраль, март, апрель, май, июнь, июль, " \
              "август, сентябрь, октябрь, ноябрь, декабрь, дело, слово, место, время, заявление, вопрос, информация," \
              " interfax ru, понедельник, вторник, среда, четверг, пятница, суббота, воскресенье"
    input_kw_ne = set([kw for kw in input_kw_ne if kw not in stop_kw])
    filtered_df = get_filtered_articles_with_kw_score(path,
                                                      sources,
                                                      source_types=source_types,
                                                      kw_ne=input_kw_ne,
                                                      regions=regions,
                                                      dates=dates,
                                                      n=2000)
    if len(filtered_df) == 0:
        return []
    cos_sim_ind_score = text_embedding.find_sim_texts(filtered_df.dropna(how="all"),
                                                      input_vec,
                                                      ref_num,
                                                      full_output=True)
    filtered_df = filtered_df.set_index("art_ind")
    sim_ind_score = kwne_similarity.get_kwne_sim(filtered_df, cos_sim_ind_score)
    sim_ind = [x[0] for x in sim_ind_score][:ref_num]
    sim_texts_df = filtered_df.loc[sim_ind]

    if len(sim_texts_df) == 0:
        return []

    sim_texts = sim_texts_df[["clean_text", "text"]].values.tolist()
    art_inds = sim_texts_df.index
    urls = sim_texts_df["url"].values

    context = extractive_summarization.lexrank_sum(sim_texts, sent_num=sent_num)
    output = []
    for i, doc in enumerate(context):
        doc_text = ""
        for sentence in doc:
            doc_text += sentence
            doc_text += " "
        output.append([art_inds[i], urls[i], doc_text])
    return output


def load_page(bert_embedding_path,
              ru_sw_file,
              ref_num_default,
              sent_num_default,
              data_path,
              otl_text_features,
              mystem_model):
    init_session_state(sent_num_default, ref_num_default, data_path)

    st.title('Генерация бекграунда')
    button_name = "Сформировать бекграунд статьи"
    input_text = st.text_area('Начните набирать текст в поле. '
                              'Когда текст готов, задайте настройки и нажмите  "%s"' % button_name,
                              height=700, key="input_text")

    if otl_text_features:
        input_kw_ne, input_vec = get_text_features_otp(input_text)
    else:
        input_kw_ne, input_vec = get_text_features(input_text, ru_sw_file, mystem_model, bert_embedding_path)

    grammar_button = st.button("Проверить правописание")
    grammar_container = st.container()

    if grammar_button:
        check_grammar_on_click(input_text, grammar_container)

    with st.expander("Параметры для генерации бекграунда", expanded=False):
        with st.form("params_form"):
            col1, col2 = st.columns(2)
            with col1:
                regions, source_types, sources, dates = filter_params_form()
            with col2:
                ref_num, sent_num, chosen_kw_ne = context_params_form(input_kw_ne)
                if len(chosen_kw_ne) == 0:
                    chosen_kw_ne = input_kw_ne
            params_form_button = st.form_submit_button("Применить настройки")
            if params_form_button:
                st.session_state["context_regions"] = regions
                st.session_state["context_types"] = source_types
                st.session_state["context_sources"] = sources
                st.session_state["context_dates"] = dates
                st.session_state["ref_num"] = ref_num
                st.session_state["sent_num"] = sent_num

    gen_button = st.button(button_name)

    if gen_button:
        output = generate_context(data_path, dates, sources, source_types, regions, input_vec, chosen_kw_ne, ref_num,
                                  sent_num)
        st.session_state["context_output"] = output
        if len(output) == 0:
            st.write("Я не нашёл подходящие под параметры фильтрации тексты. Попробуйте поменять настройки.")
    for i, doc in enumerate(st.session_state["context_output"]):
        art_ind, url, doc_text = doc
        st.markdown("[%s](%s)" % (art_ind, url))
        st.write(doc_text)
