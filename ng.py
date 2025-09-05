import streamlit as st
import os
import sys
import platform
import socket as sckt
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
type_giga_access = 'ENABLER'
type_host = 'private'
url_tok = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

sys_prompt = "Ты эмпатичный эксперт в области больших языковых моделей (LLM) и разработки программного обеспечения на языке Python, который помогает пользователю решить его проблемы и объясняет, как писать код."
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

