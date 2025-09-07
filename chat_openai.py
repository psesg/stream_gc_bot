import platform
import socket as sckt
import streamlit as st
from openai import OpenAI
# from langchain import OpenAI
# published on https://psegpt.streamlit.app/
# admin on https://share.streamlit.io/

hostname = sckt.gethostname()
plat = platform.system()
gc_model = "gpt-4o"   # "gpt-3.5-turbo"
st.title(":green[_ChatGPT_] & :blue[_Streamlit_] :red[are Great!] :sunglasses:")
st.write(f"host: :blue[{hostname}] OS: :blue[{plat}] model: :red[{gc_model}]")
# st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = gc_model

# Initialize chat history
sys_prompt = "Ты эмпатичный эксперт в области больших языковых моделей (LLM) и разработки программного обеспечения на языке Python, который помогает пользователю решить его проблемы и объясняет, как писать код. Давай ответы на русском языке."
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": sys_prompt})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
# All that's changed is that we've added a default model to st.session_state and set our OpenAI API key from Streamlit secrets. Here's where it gets interesting. We can replace our emulated stream with the model's responses from OpenAI:

    # Display assistant response in chat message container
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