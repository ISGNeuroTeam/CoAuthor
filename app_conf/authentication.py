import streamlit as st


def is_authenticated(log, log_list):
    return log in log_list


def generate_blocks(element):
    log_block = element.empty()
    inf_block = element.empty()
    vid_block = element.empty()
    return log_block, inf_block, vid_block


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def login_form(block, login_cache=""):
    # TODO: add button for text input?
    block_container = block.container()
    block_container.image("media/Soavtor Logo.png", use_column_width=False, width=300)
    block_container.subheader("Сосредоточься на истории, а не технических деталях")
    block_container.write("\n\n\n")
    return block_container.text_input(
        "Для доступа к приложению введите адрес почты, который Вы вводили при регистрации, и нажмите Enter",
        autocomplete=login_cache)


def info_form(block, info=""):
    if len(info) > 0:
        block.info(info)


def video_form(block):
    block.video("media/soavtor_2.mp4", format="video/mp4", start_time=0)


def authentication_page():
    if "login" not in st.session_state:
        st.session_state["login"] = ""
    _, center_col, _ = st.columns([1, 3, 1])
    login_block, info_block, video_block = generate_blocks(center_col)
    login = login_form(login_block, st.session_state["login"])
    if login != st.session_state["login"] and login != "":
        st.session_state["login"] = login
    info_form(info_block)
    video_form(video_block)
    return login_block, info_block, video_block
