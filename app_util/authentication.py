import streamlit as st


def generate_blocks(element):
    log_block = element.empty()
    vid_block = element.empty()
    return log_block, vid_block


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def video_form(block):
    block.video("media/soavtor_2.mp4", format="video/mp4", start_time=0)


def login_form(block, log_list, login_cache=""):
    block_container = block.container()
    block_container.image("media/Soavtor Logo.png", use_column_width=False, width=300)
    block_container.subheader("Сосредоточься на истории, а не технических деталях")
    block_container.write("\n\n\n")
    input_login = block_container.text_input(
        "Для доступа к приложению введите адрес почты, который Вы вводили при регистрации, и нажмите Enter",
        autocomplete=login_cache)
    if input_login != st.session_state["login"] and input_login != "":
        st.session_state["login"] = input_login
    if input_login in log_list:
        return True
    elif len(input_login) > 0:
        block_container.info("Почта %s не зарегистрирована" % st.session_state["login"])
    return False


def authentication_page(log_list):
    if "login" not in st.session_state:
        st.session_state["login"] = ""
    _, center_col, _ = st.columns([1, 3, 1])
    login_block, video_block = generate_blocks(center_col)
    auth_flag = login_form(login_block, log_list, login_cache="")
    video_form(video_block)
    return login_block, video_block, auth_flag
