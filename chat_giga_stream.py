import platform
import socket as sckt
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
from langchain.callbacks.base import BaseCallbackHandler

# published on https://psegiga.streamlit.app/
# admin on https://share.streamlit.io/

class StreamHandler(BaseCallbackHandler):
    def __init__(self, initial_text=""):
        pass

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"{token}", end="", flush=True)

credentials = st.secrets["my_api_key"]
gc_model = "GigaChat-2-Pro"
url_tok = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

hostname = sckt.gethostname()
plat = platform.system()

st.title(":green[_GigaChatStr_] & :blue[_Streamlit_] :red[are Great!] :sunglasses:")
st.write(f"host: :blue[{hostname}] OS: :blue[{plat}] model: :red[{gc_model}]")

rag_mode = False
rag_mode = st.checkbox("RAG", value=False)
if rag_mode:
    rag_mode = True
else:
    rag_mode = False
rag_str = "RAG is On" if rag_mode  else "RAG is Off"
st.write(rag_str)

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
                        auth_url=url_tok,
                        streaming=True,
                        callbacks = [StreamHandler()]
                        )
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        stream_resp = chat.stream(messages)
        # print(resp)
        # st.write(resp)
        response = st.write_stream(stream_resp)
    st.session_state.messages.append({"role": "assistant", "content": response})





