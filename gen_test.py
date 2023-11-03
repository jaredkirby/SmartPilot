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
    ANSWERS_PROMPT,
    ANALYZE_PROMPT,
    RESOLVE_PROMPT,
    SELECT_PROMPT,
)

load_dotenv()

model_parser = ChatOpenAI() | StrOutputParser()


chain_get_answers = ANSWERS_PROMPT | model_parser  # type: ignore

chain_analyze_answers = (
    {"question": itemgetter("question"), "answer_list": chain_get_answers}  # type: ignore
    | ANALYZE_PROMPT
    | model_parser
)

chain_resolve_answers = (
    {"question": itemgetter("question"), "analysis": chain_analyze_answers}  # type: ignore
    | RESOLVE_PROMPT
    | model_parser
)

chain_select_answer = (
    {"question": itemgetter("question"), "resolved_answers": chain_resolve_answers}  # type: ignore
    | SELECT_PROMPT
    | model_parser
)

print(chain_select_answer.invoke({"question": "What is the meaning of life?"}))
