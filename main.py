import asyncio
import streamlit as st

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

from prompt.answer import (
    ANSWER_SYS,
    ANSWER_AI,
)
from prompt.analyze import (
    ANALYZE_SYS,
)
from prompt.resolve import (
    RESOLVE_SYS,
)
from prompt.select import (
    SELECT_SYS,
)

#from dotenv import load_dotenv
openai_api_key = st.secrets["OPENAI_API_KEY"]


async def generate_multiple_initial_answers(question, n):
    print("Getting Initial Answers...")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=1.0,
        openai_api_key=openai_api_key,
    )

    answer_list = []

    sys_template = ANSWER_SYS
    answer_sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
    
    human_template= '''
Can you provide a step-by-step method to solve the following problem?
{question}

Please format your response as an outline written in the markdown language.
'''
    answer_human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    ai_template = ANSWER_AI
    answer_ai_prompt = AIMessagePromptTemplate.from_template(ai_template)

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            answer_sys_prompt,
            answer_human_prompt,
            answer_ai_prompt,
        ]
    )
    
    formatted_prompt = answer_prompt.format_prompt(
        question=question,
    ).to_messages()

    async def async_generate_answer():
        result = await asyncio.get_event_loop().run_in_executor(None, llm, formatted_prompt)
        answer = result.content.split("\n")
        return answer

    tasks = [async_generate_answer() for _ in range(n)]
    answer_list = await asyncio.gather(*tasks)
    flat_answer_list = [answer for sublist in answer_list for answer in sublist]
    answer_list = flat_answer_list
    return answer_list


def analyze_answers(question, answer_list):
    print("Analyzing Initial Answers...")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
        openai_api_key=openai_api_key,
    )

    sys_template = ANALYZE_SYS
    analyze_sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)

    analyze_template = '''
As an AI trained on a broad range of information, please analyze the following answers 
for their logic, strengths, and weaknesses:
Original Question: {question}

Answer List:
{answer_list}

Format your response as follows written in the markdown language:
Original Question: "Original Question"
- Answer Option 1: "Answer Option 1"
    - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
    - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
- Answer Option 2: "Answer Option 2"
    - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
    - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
- Answer Option 3: "Answer Option 3"
    - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
    - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
- ...

Do NOT summarize the provided Answer List in your response.
    '''
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
    llm = llm
    result = llm(formatted_prompt)

    analysis = result.content.split("\n")
    return analysis


def resolve_answers(question, analysis):
    print("Resolving Initial Answers Based on Analysis...")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.0,
        openai_api_key=openai_api_key,
    )
    sys_template = RESOLVE_SYS
    resolve_sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)

    human_template = '''
As an AI trained on a broad range of information, please help me improve the 
following answers by addressing the flaws and enhancing the strengths, based 
on the analysis provided:
Original Question: {question}

Answer List:
{analysis}

Format your response as follows written in the markdown language:
Original Question: "Original Question"
    - Updated Answer 1: "Updated Answer"
    - Updated Answer 2: "Updated Answer"
    - Updated Answer 3: "Updated Answer"
    - 
    '''
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
        openai_api_key=openai_api_key,
    )

    sys_template = SELECT_SYS
    select_sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)

    human_template = '''
As an AI trained on a broad range of information, please help me select the best 
answer for the following question from the list of answers:
Original Question: {question}

Answer List:
{resolved_answers}

Format your response as follows:
Original Question: "Original Question"
    - Selected Answer: "Selected Answer"

Do NOT summarize the answer in your response.
    '''
    select_human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    select_prompt = ChatPromptTemplate.from_messages(
        [
            select_sys_prompt, 
            select_human_prompt
        ]
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
