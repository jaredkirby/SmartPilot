import asyncio
from dotenv import load_dotenv
from operator import itemgetter

from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import (
    RunnableMap,
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)

from prompt import (
    ANSWERS_PROMPT,
    ANALYZE_PROMPT,
    RESOLVE_PROMPT,
    SELECT_PROMPT,
)

load_dotenv()

answer_model = ChatOpenAI()
model_parser = ChatOpenAI(temperature=0) | StrOutputParser()

n = 3  # Number of answers to generate

# Step 1: Generate 'n' answer options
answer_generator = RunnableMap(
    {
        f"answer_{i}": (
            {"question": RunnablePassthrough()}
            | ANSWERS_PROMPT
            | answer_model
            | StrOutputParser
        )
        for i in range(n)  # 'n' is the number of answers to generate
    }
)

print(answer_generator.invoke({"question": "What is the meaning of life?"}))
