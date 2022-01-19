import streamlit as st


def load_page():
    st.title('Архив статей')
    st.header('На этой странице можно провести поиск по всему архиву')

    # # TODO: read more than one ne and kw
    # 
    # with st.form("search_form"):
    #     st.subheader('Введите имя и/или ключевое слово. '
    #                  'Я найду все статьи, где они упоминаются отдельно или внутри другого названия.')
    #
    #     ne = st.text_input('Введите имя, место и/или название организации').strip().lower()
    #     kw = st.text_input('Введите ключевое слово').strip().lower()
    #
    #     st.form_submit_button("Поиск")
    #
    # archive_df = otp_request.get_filtered_archive(ne, kw)
    # if len(archive_df) == 0:
    #     st.write("Не удалось найти в архиве подходящие материалы, попробуйте новый поиск")
    # else:
    #     archive_df["descr"] = archive_df["descr"].apply(lambda a: a.split("%"))
    #     archive_df["_time"] = archive_df["descr"].apply(lambda a: a[0])
    #     archive_df["art_ind"] = archive_df["descr"].apply(lambda a: a[1])
    #     archive_df["topic"] = archive_df["descr"].apply(lambda a: a[2])
    #     archive_df["source"] = archive_df["descr"].apply(lambda a: a[3])
    #
    #     with st.form("filter_form"):
    #         st.subheader('Задайте фильтры')
    #         col1, col2, col3 = st.beta_columns([2, 2, 1])
    #
    #         with col1:
    #             genres = list(set(archive_df["topic"].values))
    #             topics = st.multiselect("Выберите одну или несколько тем", genres)
    #         with col3:
    #             dates = st.date_input("Введите период", value=[])
    #         with col2:
    #             sources_list = list(set(archive_df["source"].values))
    #             sources = st.multiselect('Выберите источники', sources_list)
    #
    #         st.form_submit_button("Применить фильтры")
    #
    #     if ne == "" and kw == "":
    #         ne_list = []
    #         kw_list = []
    #         index_list = []
    #     elif len(archive_df) < 50:
    #         index_list = archive_df["art_ind"].values
    #         ne_list = []
    #         kw_list = []
    #     else:
    #         st.write("Статей нашлось слишком много. Я буду искать только точные упоминания заданных слов.")
    #         ne_list = [ne]
    #         kw_list = [kw]
    #         index_list = []
    #
    #     filtered_df = otp_request.get_filtered_data_old(ne_list,
    #                                                     kw_list,
    #                                                     topics,
    #                                                     dates,
    #                                                     sources,
    #                                                     index=index_list)
    #     if len(filtered_df) > 0:
    #         filtered_df["descr"] = filtered_df["descr"].apply(lambda a: a.split("%"))
    #         filtered_df["_time"] = filtered_df["descr"].apply(lambda a: a[0])
    #         filtered_df["art_ind"] = filtered_df["descr"].apply(lambda a: a[1])
    #         filtered_df["topic"] = filtered_df["descr"].apply(lambda a: a[2])
    #         filtered_df["source"] = filtered_df["descr"].apply(lambda a: a[3])
    #
    #     if len(filtered_df) == 100:
    #         st.write("Я нашёл более 100 статей. Показываю последние 30 из них.")
    #         filtered_df = filtered_df[:30]
    #     elif len(filtered_df) > 30:
    #         st.write("Всего я нашёл %d статей. Показываю последние 30 из них." % len(filtered_df))
    #         filtered_df = filtered_df[:30]
    #     else:
    #         st.write("Всего я нашёл %d статей." % len(filtered_df))
    #
    #     if len(filtered_df) > 0:
    #         article_names = filtered_df["art_ind"].values
    #         selected_article = st.selectbox("Выберите статью, чтобы прочитать её текст", article_names)
    #         [date, title] = selected_article.split(": ")
    #
    #         article = otp_request.get_article_by_index(selected_article)["text"].values[0]
    #         article_params = filtered_df[filtered_df["art_ind"] == selected_article]
    #
    #         st.header(title)
    #         st.subheader(date)
    #         st.subheader('Рубрика: %s' % article_params["topic"].values[0])
    #         col1, _ = st.beta_columns([3, 1])
    #         with col1:
    #             st.write(article)
