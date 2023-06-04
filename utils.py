from secret import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

openai_api_key = OPENAI_API_KEY
chat_35_0 = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
chat_35_07 = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
chat_35_05 = ChatOpenAI(temperature=0.5, openai_api_key=openai_api_key)
chat_35_1 = ChatOpenAI(temperature=1, openai_api_key=openai_api_key)
chat_35_1_s = ChatOpenAI(
    temperature=1,
    openai_api_key=openai_api_key,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)
chat_4_07 = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
chat_4_05 = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.5,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
chat_4_0 = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
chat_4_0_s = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=openai_api_key,
    request_timeout=240,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)
chat_4_2 = ChatOpenAI(
    model_name="gpt-4",
    temperature=2,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
chat_4_1 = ChatOpenAI(
    model_name="gpt-4",
    temperature=1,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
chat_4_15 = ChatOpenAI(
    model_name="gpt-4",
    temperature=1.5,
    openai_api_key=openai_api_key,
    request_timeout=240,
)
