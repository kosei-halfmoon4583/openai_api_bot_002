# 以下を「pgi.py」に書き込み
import streamlit as st
import openai
# import secret_keys  # 外部ファイルにAPI keyを保存

# openai.api_key = secret_keys.openai_api_key
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
system_prompt = st.secrets.content.system_prompt

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

#    response = openai.ChatCompletion.create(
# 2023/11/25 update.
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

#    bot_message = response["choices"][0]["message"]
# 2023/11/25 update 
    bot_message = response.choices[0].message.content
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# User Interface
import streamlit as st
st.image("PGI_image03.png")
st.subheader("PGI :blue[プログラミング] 講師 :sunglasses:")
st.write("プログラミングに関してお答えします。質問をどうぞ！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
# 直近のメッセージを上に表示する
    for message in reversed(messages[1:]):
        speaker = "😎"
#        if message["role"]=="assistant":
#        if message[0]=="assistant":
#            speaker="👽"

#        st.write(speaker + ": " + message["content"])
        st.write(speaker + ": " + message[1])
