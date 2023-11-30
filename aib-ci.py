# 以下を「aib-ci(code interpreter).py」に書き込み
import streamlit as st
from openai import OpenAI

# client = OpenAI()

client = OpenAI(
  organization='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',
)

# 外部ファイルにAPI keyを保存
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
# System promptsをstreamlitのconfig(secrets)に保存
system_prompt = st.secrets.content.system_prompt

# Save messages to st.session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
    ]

# assistant : code interpreter 設定
assistant = client.beta.assistants.create(
  instructions="You're personal programming tutor. You will provided with a piece of code, and your task is to explain it in a concise way.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)

# Function of ChatGPT API communication.
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# User Interface
import streamlit as st
st.image("PGI_image03.png")
st.subheader("PGI :blue[code interpreter] :sunglasses:")
st.write("You're personal programming tutor. You will provided with a piece of code, and your task is to explain it in a concise way.")

user_input = st.text_input("Please input the code", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
# 直近のメッセージを上に表示する
    for message in reversed(messages[1:]):
        speaker = ""
        if message["role"]=="assistant":
            speaker=""

        st.write(speaker + ": " + message["content"])
