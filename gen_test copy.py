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


# Async function to generate multiple initial answers


def generate_answers(question, n):
    llm = ChatOpenAI()
    answer_chain = RunnableParallel(*[llm for _ in range(n)])
    answer_options = answer_chain.invoke([{"prompt": question} for _ in range(n)])
    concatenated_answers = " ".join([option["content"] for option in answer_options])
    return concatenated_answers


async def generate_multiple_initial_answers(input_dict):
    question = input_dict["question"]
    n = input_dict["n"]
    # Define the runnable chain with the model
    answers_chain = ANSWERS_PROMPT | answer_model

    # Format and invoke the chain asynchronously
    async def generate_answer():
        return await answers_chain.ainvoke({"question": question})

    # Generate multiple answers asynchronously
    tasks = [generate_answer() for _ in range(n)]
    answer_list = await asyncio.gather(*tasks)

    # Flatten the list of answers
    flat_answer_list = [answer.content.split("\n") for answer in answer_list]
    flat_answer_list = [item for sublist in flat_answer_list for item in sublist]
    return flat_answer_list


async def process_question(input_dict):
    # Generate multiple initial answers
    flat_answer_list = await generate_multiple_initial_answers(input_dict)

    # Analyze the answers
    RunnableLambda(
        analysis=(
            ({"question": input_dict["question"], "answer_list": flat_answer_list})
            | ANALYZE_PROMPT
            | model_parser
        )
    )

    # Resolve the answers

    RunnableLambda(
        resolved_answers=(
            ({"question": input_dict["question"], "analysis": analysis})
            | RESOLVE_PROMPT
            | model_parser
        )
    )

    # Select the best answer
    RunnableLambda(
        selected_answer=(
            ({"question": input_dict["question"], "resolved_answers": resolved_answers})
            | SELECT_PROMPT
            | model_parser
        )
    )

    return selected_answer


# Test the function
print(
    asyncio.run(process_question({"question": "What is the meaning of life?", "n": 3}))
)


"""
chain_analyze_answers = (
    {"question": itemgetter("question"), "answer_list": flat_answer_list}  # type: ignore
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
"""
