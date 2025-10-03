# -*- coding: utf-8 -*-

import os
import sys
import streamlit as st
import logging

# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
from giga_util import get_giga_credentials, get_giga_url_access_mode

# published on https://psegiga.streamlit.app/
# admin on https://share.streamlit.io/

# set logging level - for logging to file add: filename='myapp.log',
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore") # default Change the filter in this process
    os.environ["PYTHONWARNINGS"] = "ignore" # ignore Also affect subprocesses

# get credentials from переменной окружения `GIGACHAT_CREDENTIALS`
credentials = get_giga_credentials()
if credentials == '':
    exit(1)

# get url_oauth and access_mode
url_oauth, access_mode = get_giga_url_access_mode()
type_host = access_mode['type_host']
type_giga_access = access_mode['type_giga_access']
hostname = access_mode['hostname']
plat = access_mode['plat']

gc_model = "GigaChat-2-Pro"

st.title(":green[_GigaChat_] & :blue[_Streamlit_] :red[are Great!] :sunglasses:")
st.write(f"host: :blue[{hostname}] OS: :blue[{plat}] model: :red[{gc_model}] zone: :green[{type_giga_access}]")

# Set a default model
if "ai_model" not in st.session_state:
    st.session_state["ai_model"] = gc_model

# Initialize chat history
sys_prompt = "Ты эмпатичный эксперт в области больших языковых моделей (LLM) и разработки программного обеспечения на языке Python, который помогает пользователю решить его проблемы и объясняет, как писать код."
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

        chat = GigaChat(model=gc_model,
                        credentials=credentials,
                        verify_ssl_certs=False,
                        scope="GIGACHAT_API_CORP",
                        auth_url=url_oauth
                        )
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        resp = chat.invoke(messages).content
        print(resp)
        st.write(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})