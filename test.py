from dotenv import load_dotenv
import os

# .envファイルの読み込み
load_dotenv()

# 環境変数を取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")


import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.callbacks import get_openai_callback

def init_page():
    st.set_page_config(
        page_title="RI_AI_Agent",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")
    st.sidebar.title("Options")

def init_message():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []

def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3", "GPT-4o", "GPT-4o-mini"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo-0125"

    elif model == "GPT-4o":
        model_name = "gpt-4o-2024-08-06"

    else:
        model_name = "gpt-4o-mini-2024-07-18"

    temperature = st.sidebar.slider("temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

    return ChatOpenAI(temperature=temperature, model_name=model_name)

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost




def main():
    # 初期化
    init_page()
    llm = select_model()
    init_message()

    # ユーザーの入力を監視
    if user_input := st.chat_input("RIの業務について聞きたいことを入力してください。"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")


if __name__ == '__main__':
    main()


