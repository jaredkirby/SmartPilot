import asyncio
from dotenv import load_dotenv
from operator import itemgetter

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

from prompt import (
    ANSWERS_SYS,
    ANSWERS_HUM,
    ANSWERS_AI,
    ANSWERS_PROMPT,
    ANALYZE_SYS,
    ANALYZE_HUM,
    ANALYZE_PROMPT,
    RESOLVE_SYS,
    RESOLVE_HUM,
    RESOLVE_PROMPT,
    SELECT_SYS,
    SELECT_HUM,
    SELECT_PROMPT,
)

load_dotenv()

model_parser = ChatOpenAI() | StrOutputParser()


chain_get_answers = ANSWERS_PROMPT | model_parser  # type: ignore

chain_analyze_answers = ANALYZE_PROMPT | model_parser  # type: ignore

chain_resolve_answers = RESOLVE_PROMPT | model_parser  # type: ignore

chain_select_answer = SELECT_PROMPT | model_parser  # type: ignore

chain = (
    {"question": itemgetter("question"), "answer_list": chain_get_answers}
    | {"analysis": chain_analyze_answers}
    | {"resolved_answers": chain_resolve_answers}
    | chain_select_answer  # type: ignore
)

print(chain.invoke({"question": "What is the meaning of life?"}))
