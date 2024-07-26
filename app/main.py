import streamlit as st

from gigachat_api import get_access_token, send_prompt

st.title("Чат бот")

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("Получил токен")
    except Exception as e:
        st.toast(f"Не получилось получить токен: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "С чем вам помочь?"}]

for msg in st.session_state.messages:
    if msg.get("is_image"):
        st.chat_message(msg["role"]).image(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if user_prompt := st.chat_input():
    st.chat_message("user").write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner("В процессе..."):
        response = send_prompt(user_prompt, st.session_state.access_token)
        st.chat_message("ai").write(response)
        st.session_state.messages.append({"role": "ai", "content": response})
