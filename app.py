import streamlit as st
import numpy as np
import os
import sys
import platform
import socket as sckt
import requests
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore") # default Change the filter in this process
    os.environ["PYTHONWARNINGS"] = "ignore" # ignore Also affect subprocesses

plat = platform.system()
type_giga_access = ""
userdomain = ""
type_host = ""
hostname = sckt.gethostname()

if plat == "Windows": # Windows
    try:
        userdomain = os.environ['USERDOMAIN']
    except KeyError:
        pass
    else:
        if userdomain.upper() == 'SIGMA':
            type_giga_access = 'SIGMA'
            type_host = 'corporate'
        else:
            type_giga_access = 'ENABLER'
            type_host = 'private'

if plat == "Darwin":  #
    if hostname.startswith('cab-ws'):
        type_giga_access = 'SIGMA'
        type_host = 'corporate'
    else:
        type_giga_access = 'ENABLER'
        type_host = 'private'

url_tok = ""
if type_giga_access == 'SIGMA':
    url_tok = "https://sm-auth-sd.prom-88-89-apps.ocp-geo.ocp.sigma.sbrf.ru/api/v2/oauth"
if type_giga_access == 'ENABLER':
    url_tok = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

sys_prompt = "Ты эмпатичный эксперт в области разработки программного обеспечения на языке Python, который помогает пользователю решить его проблемы и объясняет, как писать код."
gc_model = "GigaChat-2-Pro"
credentials = st.secrets["my_api_key"]
# Авторизация в сервисе GigaChat
chat = GigaChat(model=gc_model,
                credentials=credentials,
                verify_ssl_certs=False,
                scope="GIGACHAT_API_CORP",
                auth_url=url_tok)

messages = [
    SystemMessage(
        content=sys_prompt
    )
]

st.title(":green[_GigaChat_] & :blue[_Streamlit_] :red[are Great!] :sunglasses:")
st.write(f"mode: :blue[{type_host}] host: :blue[{hostname}] OS: :blue[{plat}] model: :red[{gc_model}] zone: :green[{type_giga_access}]")

with st.container(border=True):
    # st.write("This is inside the container")
    title = st.text_area("системный промпт", sys_prompt)
    # dialog = st.text_area("диалог с ботом", '', key="dlg")
    user_input = ''
    # while(True):
    user_input = st.text_input("введите свой вопрос", "", key="uinput")
    # if user_input == '':
    #     break
    messages.append(HumanMessage(content=user_input))
    res = chat.invoke(messages)
    messages.append(res)
    print("Bot: ", res.content)
    dialog = st.text_area("диалог с ботом", f"Вы: {user_input}\nBot: {res.content}\n", key="dlg")
    # You can call any Streamlit command, including custom components:
    # st.bar_chart(np.random.randn(50, 3))

