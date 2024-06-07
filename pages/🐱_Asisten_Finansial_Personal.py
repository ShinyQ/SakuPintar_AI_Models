import streamlit as st
from openai import OpenAI
from utils.config import OPENAI_API_TOKEN

st.title("🐱 Meowney")
st.text("Yuk! Tanyakan Soal Keuangan Apapun pada Meowney!")

# Initialize session state if not already done
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Kamu adalah seorang manajer keuangan bernama meowny yang expert dan membalas klien dalam bahasa Indonesia.",
        },
        {
            "role": "assistant",
            "content": "Halo, ada yang bisa Meowny bantu?",
        },
    ]

if "response" not in st.session_state:
    st.session_state["response"] = None

# Display chat messages
messages = st.session_state.messages
for msg in messages:
    if msg.get('role') != 'system':
        st.chat_message(msg["role"]).write(msg["content"])

# Handle user input and generate response
if prompt := st.chat_input(placeholder="Halo Meowny, apa perbedaan obligasi dan saham?"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=OPENAI_API_TOKEN)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    st.session_state["response"] = response.choices[0].message.content

    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])