import asyncio

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from utils import (
    chat_35_1,
    chat_35_0,
    chat_4_0,
)

intial_llm = chat_35_1
analyze_llm = chat_4_0
resolve_llm = chat_4_0
select_llm = chat_4_0


async def generate_multiple_initial_answers(question, n, llm=intial_llm):
    answer_list = []

    answer_sys_prompt = """
You are AnswerPilot, a large language model trained by OpenAI and prompt
engineered by Jared Kirby.
Your task is to provide detailed, step-by-step answers to the question.
Use reliable sources, do not fabricate information.
Remember, the goal is to produce high-quality, reliable, and accurate responses.
"""
    answer_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        answer_sys_prompt
    )

    answer_human_prompt = PromptTemplate(
        template="""
Question: Can you provide a step-by-step method to solve the following problem?
{question}
    """,
        input_variables=["question"],
    )
    answer_human_message_prompt = HumanMessagePromptTemplate(prompt=answer_human_prompt)

    answer_ai_prompt = """
Sure, let's break down the problem and work through it step by step to arrive
at the correct solution.

Here are the steps: ...
"""
    answer_ai_message_prompt = AIMessagePromptTemplate.from_template(answer_ai_prompt)

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            answer_sys_message_prompt,
            answer_human_message_prompt,
            answer_ai_message_prompt,
        ]
    )
    answer_chain = LLMChain(verbose=True, llm=llm, prompt=answer_prompt)

    async def async_generate_answer(chain, question):
        answer = await chain.arun({"question": question})
        answer = answer.split("\n")
        return answer

    tasks = [async_generate_answer(answer_chain, question) for _ in range(n)]
    answer_list = await asyncio.gather(*tasks)
    flat_answer_list = [answer for sublist in answer_list for answer in sublist]
    answer_list = flat_answer_list

    return answer_list


def analyze_answers(question, answer_list, llm=analyze_llm):
    analyze_sys_prompt = """
You are AnalyzePilot, a large language model trained by OpenAI and prompt
engineered by Jared Kirby. Your task is to analyze the answers provided, 
identifying the flaws and strengths in logic for each answer option. 
Remember to use a systematic, step-by-step approach to ensure all aspects are 
considered. Do NOT summarize the provided Asnwer List in your response.
Present your response in a structured format, as outlined below.
"""
    analyze_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        analyze_sys_prompt
    )

    analyze_human_prompt = PromptTemplate(
        template="""
As an AI trained on a broad range of information, please analyze the following answers 
for their logic, strengths, and weaknesses:
Original Question: {question}

Answer List:
{answer_list}

Format your response as follows:
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
    """,
        input_variables=["question", "answer_list"],
    )
    analyze_human_message_prompt = HumanMessagePromptTemplate(
        prompt=analyze_human_prompt
    )

    analyze_prompt = ChatPromptTemplate.from_messages(
        [analyze_sys_message_prompt, analyze_human_message_prompt]
    )
    analyze_chain = LLMChain(verbose=True, llm=llm, prompt=analyze_prompt)
    analysis = analyze_chain.run({"question": question, "answer_list": answer_list})
    analysis = analysis.split("\n")
    return analysis


def resolve_answers(question, analysis, llm=resolve_llm):
    resolve_sys_prompt = """
You are ResolvePilot, a large language model trained by OpenAI and prompt
engineered by Jared Kirby. Your task is to analyze the question and answer 
data provided to you, and resolve each answer by addressing the flaws and 
enhancing the strengths identified. Remember to work systematically and 
step by step, using reliable information. The response should be formatted 
as outlined below.
"""
    resolve_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        resolve_sys_prompt
    )

    resolve_human_prompt = PromptTemplate(
        template="""
As an AI trained on a broad range of information, please help me improve the 
following answers by addressing the flaws and enhancing the strengths, based 
on the analysis provided:
Original Question: {question}

Answer List:
{analysis}

Format your response as follows:
Original Question: "Original Question"
    - Updated Answer 1: "Updated Answer"
    - Updated Answer 2: "Updated Answer"
    - Updated Answer 3: "Updated Answer"
    - ...
    """,
        input_variables=["question", "analysis"],
    )
    resolve_human_message_prompt = HumanMessagePromptTemplate(
        prompt=resolve_human_prompt
    )

    resolve_prompt = ChatPromptTemplate.from_messages(
        [resolve_sys_message_prompt, resolve_human_message_prompt]
    )
    resolve_chain = LLMChain(verbose=True, llm=llm, prompt=resolve_prompt)
    resolved_answers = resolve_chain.run({"question": question, "analysis": analysis})
    return resolved_answers


def select_answer(question, resolved_answers, llm=select_llm):
    select_sys_prompt = """
You are SelectPilot, a large language model trained by OpenAI and prompt
engineered by Jared Kirby. Your task is to analyze the original question 
and the list of answers provided, and then select the best answer based 
on the information given. Remember to work systematically and step by step, 
using reliable information.
The response should be formatted as outlined below.
"""
    select_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        select_sys_prompt
    )

    select_human_prompt = PromptTemplate(
        template="""
As an AI trained on a broad range of information, please help me select the best 
answer for the following question from the list of answers:
Original Question: {question}

Answer List:
{resolved_answers}

Format your response as follows:
Original Question: "Original Question"
    - Selected Answer: "Selected Answer"

Do NOT summarize the aswer in your response.
    """,
        input_variables=["question", "resolved_answers"],
    )
    select_human_message_prompt = HumanMessagePromptTemplate(prompt=select_human_prompt)

    select_prompt = ChatPromptTemplate.from_messages(
        [select_sys_message_prompt, select_human_message_prompt]
    )
    select_chain = LLMChain(verbose=True, llm=llm, prompt=select_prompt)
    selected_answer = select_chain.run(
        {"question": question, "resolved_answers": resolved_answers}
    )
    return selected_answer


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
