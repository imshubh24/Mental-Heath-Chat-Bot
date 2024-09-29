from openai import OpenAI
import streamlit as st


# Setting page configuration
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🤖", layout="centered")

# Sidebar for additional information
st.sidebar.title("Mental Health Support Bot")
st.sidebar.write("Welcome to the Mental Health Chatbot! We're here to listen and assist you.")

# Main header
st.title("Mental Health Chatbot")
st.subheader("Let's talk about how you're feeling today!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask your Questions!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})