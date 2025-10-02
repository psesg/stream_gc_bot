# -*- coding: utf-8 -*-

import streamlit as st
import os
import sys
import logging
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from giga_util import get_giga_credentials, get_giga_url_access_mode


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

sys_prompt = "Ты эмпатичный эксперт в области больших языковых моделей (LLM) и разработки программного обеспечения на языке Python, который помогает пользователю решить его проблемы и объясняет, как писать код."
gc_model = "GigaChat-2-Pro"
# credentials = st.secrets["my_api_key"]
# Авторизация в сервисе GigaChat
chat = GigaChat(model=gc_model,
                credentials=credentials,
                verify_ssl_certs=False,
                scope="GIGACHAT_API_CORP",
                auth_url=url_oauth)

messages = [
    SystemMessage(
        content=sys_prompt
    )
]

st.title(":green[_GigaChat_] & :blue[_Streamlit_] :red[are Great!] :sunglasses:")
st.write(f"mode: :blue[{type_host}] host: :blue[{hostname}] OS: :blue[{plat}] model: :red[{gc_model}] zone: :green[{type_giga_access}]")

with st.container(border=True):
    title = st.text_area("системный промпт", sys_prompt)
    user_input = ''
    user_input = st.text_input("введите свой вопрос", "", key="uinput")
    messages.append(HumanMessage(content=user_input))
    res = chat.invoke(messages)
    messages.append(res)
    print("Bot: ", res.content)
    dialog = st.text_area("диалог с ботом", f"Вы: {user_input}\nBot: {res.content}\n", key="dlg")


