import asyncio
from tqdm import tqdm
from dotenv import load_dotenv

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import ConfigurableField
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

from langserve import add_routes
from operator import itemgetter
import asyncio

from prompt import (
    ANSWERS_PROMPT,
    ANALYZE_PROMPT,
    RESOLVE_PROMPT,
    SELECT_PROMPT,
)

load_dotenv()

app = FastAPI(
    title="SmartPilot",
    version="0.3",
    description="SmartPilot uses LLMs to generate, analyze, and select the best answer to a given question.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

answers_model = ChatOpenAI(temperature=0.5).configurable_alternatives(
    ConfigurableField(
        id="llm",
        name="LLM",
        description=(
            "Decide whether to use a high or a low temperature parameter for generating the initial set of answers."
        ),
    ),
    high_temp=ChatOpenAI(temperature=0.9),
    low_temp=ChatOpenAI(temperature=0.1),
    default_key="medium_temp",
)

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.runnables import RunnableMap
import asyncio

# Assume the necessary prompt templates are defined and available
model = ChatOpenAI()


# Async function to generate multiple initial answers
async def generate_multiple_initial_answers(question, n):
    # Define prompt templates
    answer_sys_prompt = SystemMessagePromptTemplate.from_template(ANSWER_SYS)
    answer_human_prompt = HumanMessagePromptTemplate.from_template(ANSWER_HUM)
    answer_ai_prompt = AIMessagePromptTemplate.from_template(ANSWER_AI)

    # Combine the prompts into a single chain
    answer_prompt_chain = RunnableMap(
        {
            "system_message": answer_sys_prompt,
            "human_message": answer_human_prompt,
            "ai_message": answer_ai_prompt,
        }
    )

    # Define the runnable chain with the model
    answer_chain = answer_prompt_chain | model

    # Format and invoke the chain asynchronously
    async def generate_answer():
        formatted_prompt = {
            "system_message": {"content": ANSWER_SYS.format(question=question)},
            "human_message": {"content": ANSWER_HUM.format(question=question)},
            "ai_message": {"content": ANSWER_AI.format(question=question)},
        }
        return await answer_chain.ainvoke(formatted_prompt)

    # Generate multiple answers asynchronously
    tasks = [generate_answer() for _ in range(n)]
    answer_list = await asyncio.gather(*tasks)

    # Flatten the list of answers
    flat_answer_list = [answer.content.split("\n") for answer in answer_list]
    flat_answer_list = [item for sublist in flat_answer_list for item in sublist]
    return flat_answer_list


# Async function to analyze the answers
async def analyze_answers(question, answer_list):
    # Define analysis chain
    analyze_chain = analyze_sys | analyze_human | model
    # Format the chat prompt
    formatted_prompt = {
        "system_message": {"content": ANALYZE_SYS.format(question=question)},
        "human_message": {
            "content": ANALYZE_HUM.format(question=question, answer_list=answer_list)
        },
    }
    # Invoke the analysis chain asynchronously
    analysis = await analyze_chain.ainvoke(formatted_prompt)
    return analysis.content.split("\n")


# Async function to resolve the answers
async def resolve_answers(question, analysis):
    # Define resolution chain
    resolve_chain = resolve_sys | resolve_human | model
    # Format the chat prompt
    formatted_prompt = {
        "system_message": {"content": RESOLVE_SYS.format(question=question)},
        "human_message": {
            "content": RESOLVE_HUM.format(question=question, analysis=analysis)
        },
    }
    # Invoke the resolve chain asynchronously
    resolved = await resolve_chain.ainvoke(formatted_prompt)
    return resolved.content.split("\n")


# Async function to select the best answer
async def select_best_answer(question, resolved_answers):
    # Define selection chain
    select_chain = select_sys | select_human | model
    # Format the chat prompt
    formatted_prompt = {
        "system_message": {"content": SELECT_SYS.format(question=question)},
        "human_message": {
            "content": SELECT_HUM.format(
                question=question, resolved_answers=resolved_answers
            )
        },
    }
    # Invoke the select chain asynchronously
    selected = await select_chain.ainvoke(formatted_prompt)
    return selected.content


# Main async function to orchestrate the process
async def orchestrate_process(question, n_answers):
    # 1. Generate Answers
    answers = await generate_multiple_initial_answers(question, n_answers)

    # 2. Analyze the Answers
    analysis = await analyze_answers(question, answers)

    # 3. Resolve the Answer Analysis
    resolved = await resolve_answers(question, analysis)

    # 4. Select the Best Answer
    best_answer = await select_best_answer(question, resolved)

    return best_answer


# Example usage
question = "Explain the process of photosynthesis."
number_of_answers = 5

# Run the orchestration async function in an event loop
asyncio.run(orchestrate_process(question, number_of_answers))


async def generate_multiple_initial_answers(question, n, llm=answers_model):
    # Create a list of answers
    answer_list = []
    # Create prompt templates
    answer_sys_prompt = SystemMessagePromptTemplate.from_template(ANSWER_SYS)
    human_template = ANSWER_HUM
    answer_human_prompt = HumanMessagePromptTemplate.from_template(human_template)
    answer_ai_prompt = AIMessagePromptTemplate.from_template(ANSWER_AI)
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            answer_sys_prompt,
            answer_human_prompt,
            answer_ai_prompt,
        ]
    )
    # Format the chat prompt
    formatted_prompt = answer_prompt.format_prompt(
        question=question,
    ).to_messages()

    # Generate multiple answers
    async def async_generate_answer():
        result = await asyncio.get_event_loop().run_in_executor(
            None, llm, formatted_prompt
        )
        answer = result.content.split("\n")
        return answer

    tasks = [async_generate_answer() for _ in range(n)]
    with tqdm(total=n) as pbar:
        for future in asyncio.as_completed(tasks):
            answer = await future
            answer_list.append(answer)
            pbar.update(1)

    # Flatten the list of answers
    flat_answer_list = [answer for sublist in answer_list for answer in sublist]
    answer_list = flat_answer_list
    return answer_list


# Use function call
def analyze_answers(question, answer_list):
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
    )
    analyze_sys_prompt = SystemMessagePromptTemplate.from_template(ANALYZE_SYS)
    analyze_template = ANALYZE_HUM
    analyze_human_prompt = HumanMessagePromptTemplate.from_template(analyze_template)
    analyze_prompt = ChatPromptTemplate.from_messages(
        [
            analyze_sys_prompt,
            analyze_human_prompt,
        ]
    )
    formatted_prompt = analyze_prompt.format_prompt(
        question=question,
        answer_list=answer_list,
    ).to_messages()

    result = llm(formatted_prompt)
    analysis = result.content.split("\n")
    return analysis


def resolve_answers(question, analysis):
    print("Resolving Initial Answers Based on Analysis...")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
    )
    resolve_sys_prompt = SystemMessagePromptTemplate.from_template(RESOLVE_SYS)
    human_template = RESOLVE_HUM
    resolve_human_prompt = HumanMessagePromptTemplate.from_template(human_template)
    resolve_prompt = ChatPromptTemplate.from_messages(
        [
            resolve_sys_prompt,
            resolve_human_prompt,
        ]
    )
    formatted_prompt = resolve_prompt.format_prompt(
        question=question,
        analysis=analysis,
    ).to_messages()
    llm = llm
    resolved_answers = llm(formatted_prompt)
    return resolved_answers.content


def select_answer(question, resolved_answers):
    print("Selecting Best Answer...")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
    )
    select_sys_prompt = SystemMessagePromptTemplate.from_template(SELECT_SYS)
    human_template = SELECT_HUM
    select_human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    select_prompt = ChatPromptTemplate.from_messages(
        [select_sys_prompt, select_human_prompt]
    )
    formatted_prompt = select_prompt.format_prompt(
        question=question,
        resolved_answers=resolved_answers,
    ).to_messages()
    llm = llm
    selected_answer = llm(formatted_prompt)
    return selected_answer.content


async def main():
    # Ask the user for the question and iteration number 'n'
    question = input("What is your question? ")
    n = int(input("How many answers do you want? "))

    # Generate 'n' answers to the question
    answer_list = await generate_multiple_initial_answers(question, n)
    print("Generated answers:", answer_list)

    # Analyze all answers
    analysis = analyze_answers(question, answer_list)
    print("Analysis of answers:", analysis)

    # Resolve answers using analysis from analyze_answers()
    resolved_answers = resolve_answers(question, analysis)
    print("Resolved answers:", resolved_answers)

    # Select the best answer from the resolved answers
    selected_answer = select_answer(question, resolved_answers)
    print("Selected best answer:", selected_answer)


if __name__ == "__main__":
    asyncio.run(main())
