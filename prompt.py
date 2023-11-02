from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

# Generate multiple initial answers
answers_sys = SystemMessagePromptTemplate.from_template(
    """ \
You are AnswerPilot, a large language model trained by OpenAI and prompt \
engineered by Jared Kirby.
Your task is to provide detailed, step-by-step answers to the question.
Use reliable sources and do not fabricate information.
Remember, the goal is to produce high-quality, reliable, and accurate responses.
"""
)

answers_human = HumanMessagePromptTemplate.from_template(
    """ \
Can you provide a step-by-step method to solve the following problem?
{question}

Please format your response as an outline written in Markdown.
"""
)

answers_ai = AIMessagePromptTemplate.from_template(
    """ \
Sure, let's break down the problem and work through it step by step to arrive \
at the correct solution.

Here are the steps:
"""
)

ANSWERS_PROMPT = ChatPromptTemplate.from_messages(
    [answers_sys, answers_human, answers_ai]
)

# Analyze the answers
analyze_sys = SystemMessagePromptTemplate.from_template(
    """ \
You are AnalyzePilot, a large language model trained by OpenAI and prompt \
engineered by Jared Kirby. Your task is to analyze the answers \
provided, identifying the flaws and strengths in logic for each answer option. 
Remember to use a systematic, step-by-step approach to ensure all aspects are \
considered. Do NOT summarize the provided Answer List in your response.
Present your response in a structured format, as outlined below.
"""
)

analyze_human = HumanMessagePromptTemplate.from_template(
    """ \
As an AI trained on a broad range of information, please analyze the following answers \
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
    """
)

ANALYZE_PROMPT = ChatPromptTemplate.from_messages([analyze_sys, analyze_human])

# Resolve the answers analysis
resolve_sys = SystemMessagePromptTemplate.from_template(
    """ \
You are ResolvePilot, a large language model trained by OpenAI and prompt \
engineered by Jared Kirby. Your task is to analyze the question and answer \
data provided to you, and resolve each answer by addressing the flaws and \
enhancing the strengths identified. Remember to work systematically and \
step by step, using reliable information. The response should be formatted \
as outlined below.
"""
)

resolve_human = HumanMessagePromptTemplate.from_template(
    """ \
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
    """
)

RESOLVE_PROMPT = ChatPromptTemplate.from_messages([resolve_sys, resolve_human])

# Select the best answer
select_sys = SystemMessagePromptTemplate.from_template(
    """ \
You are SelectPilot, a large language model trained by OpenAI and prompt \
engineered by Jared Kirby. Your task is to analyze the original question \
and the list of answers provided, and then select the best answer based \
on the information given. Remember to work systematically and \
step by step using reliable information.
The response should be formatted as outlined below.
"""
)

select_human = HumanMessagePromptTemplate.from_template(
    """ \
As an AI trained on a broad range of information, please help me select the best \
answer for the following question from the list of answers:
Original Question: {question}

Answer List:
{resolved_answers}

Format your response as follows:
Original Question: "Original Question"
    - Selected Answer: "Selected Answer"

Do NOT summarize the answer in your response.
    """
)

SELECT_PROMPT = ChatPromptTemplate.from_messages([select_sys, select_human])
