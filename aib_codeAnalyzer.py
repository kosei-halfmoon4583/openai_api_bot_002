
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
system_prompt = st.secrets.content.system_prompt

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
col1, col2 = st.beta_columns(2)

with col1:
    st.title("AIB :blue[Assistant] :sunglasses:　")

with col2:
    date = st.date_input("Pick a date")

st.write("OpenAI APIを利用したアシスタントAIです。複雑な文章を要約したり、理解しやすく修正してくれたりします。")

user_input = st.text_input("解析したい文章などを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
# 直近のメッセージを上に表示する
    for message in reversed(messages[1:]):
        speaker = "😎"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
