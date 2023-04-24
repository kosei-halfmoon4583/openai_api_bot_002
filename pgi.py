# 以下を「pgi.py」に書き込み
import streamlit as st
import openai
# import secret_keys  # 外部ファイルにAPI keyを保存

# openai.api_key = secret_keys.openai_api_key
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
system_prompt = st.secrets.content.system_prompt

# system_prompt = """
# あなたは優秀なプログラミング講師です。
# プログラミング上達のために、生徒のレベルに合わせて適切なアドバイスを行ってください。
# あなたの役割は生徒のプログラミングスキルを向上させることなので、例えば以下のようなプログラミング以外のことを聞かれても、絶対に答えないでください。
#
# * 旅行
# * 料理
# * 芸能人
# * 映画
# * 科学
# * 歴史
# """

# Save messages to st.session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]

# Function of ChatGPT API communication.
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

# User Interface
import streamlit as st

st.subheader('This is a subheader')
st.subheader('A subheader with _italics_ :blue[colors] and emojis :sunglasses:')
st.image("04_programming.jpg")
st.subheader(" 「:gray[PGI]:blue[プログラミング]:gray[講師]」")
st.write("プログラミングに関して、何でも聞いてください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
# 直近のメッセージを上に表示する
    for message in reversed(messages[1:]):  
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
