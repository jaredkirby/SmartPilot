"""SmartPilot main module - AI-powered question answering system using OpenAI Responses API."""

import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

from .prompts import (
    ANALYZE_SYSTEM,
    ANSWER_ASSISTANT_PREFIX,
    ANSWER_SYSTEM,
    RESOLVE_SYSTEM,
    SELECT_SYSTEM,
)

# Load environment variables
load_dotenv()

# Default model - GPT-5 Mini
DEFAULT_MODEL = "gpt-4.1-mini"


def get_client() -> OpenAI:
    """Get OpenAI client instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def generate_response(
    client: OpenAI,
    system_prompt: str,
    user_message: str,
    temperature: float = 0.7,
    model: Optional[str] = None,
    assistant_prefix: Optional[str] = None,
) -> str:
    """Generate a response using OpenAI Responses API.

    Args:
        client: OpenAI client instance
        system_prompt: System prompt to guide the model
        user_message: User's question or input
        temperature: Sampling temperature (0.0-2.0)
        model: Model to use (defaults to DEFAULT_MODEL)
        assistant_prefix: Optional prefix for assistant response

    Returns:
        Generated response text
    """
    model = model or DEFAULT_MODEL
    input_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    if assistant_prefix:
        input_messages.append({"role": "assistant", "content": assistant_prefix})

    response = client.responses.create(
        model=model,
        input=input_messages,
        temperature=temperature,
    )

    return response.output_text


async def generate_single_answer(
    client: OpenAI,
    question: str,
    model: Optional[str] = None,
) -> str:
    """Generate a single answer to a question asynchronously.

    Args:
        client: OpenAI client instance
        question: The question to answer
        model: Model to use

    Returns:
        Generated answer
    """
    user_message = f"""\
Please provide a step-by-step method to solve the following problem:

{question}

Format your response as a clear outline in Markdown.
"""

    # Run in executor to make it async
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: generate_response(
            client=client,
            system_prompt=ANSWER_SYSTEM,
            user_message=user_message,
            temperature=1.0,
            model=model,
            assistant_prefix=ANSWER_ASSISTANT_PREFIX,
        ),
    )
    return result


async def generate_multiple_initial_answers(
    question: str,
    n: int,
    model: Optional[str] = None,
) -> list[str]:
    """Generate multiple initial answers to a question.

    Args:
        question: The question to answer
        n: Number of answers to generate
        model: Model to use

    Returns:
        List of generated answers
    """
    client = get_client()
    answer_list = []

    tasks = [generate_single_answer(client, question, model) for _ in range(n)]

    with tqdm(total=n, desc="Generating answers") as pbar:
        for future in asyncio.as_completed(tasks):
            answer = await future
            answer_list.append(answer)
            pbar.update(1)

    return answer_list


def analyze_answers(
    question: str,
    answer_list: list[str],
    model: Optional[str] = None,
) -> str:
    """Analyze the generated answers for strengths and weaknesses.

    Args:
        question: Original question
        answer_list: List of generated answers
        model: Model to use

    Returns:
        Analysis of all answers
    """
    client = get_client()

    # Format answers for analysis
    formatted_answers = "\n\n".join(
        [f"### Answer Option {i + 1}:\n{answer}" for i, answer in enumerate(answer_list)]
    )

    user_message = f"""\
Please analyze the following answers for their logic, strengths, and weaknesses.

## Original Question:
{question}

## Answer Options:
{formatted_answers}

## Analysis Format:
For each answer option, provide:
- **Answer Option N Summary**: Brief summary of the approach
- **Identified Strengths**: List specific strengths with explanations
- **Identified Weaknesses**: List specific flaws or areas for improvement
- **Overall Assessment**: Brief evaluation of the answer quality

Be thorough but concise. Do NOT rewrite the answers, only analyze them.
"""

    return generate_response(
        client=client,
        system_prompt=ANALYZE_SYSTEM,
        user_message=user_message,
        temperature=0.0,
        model=model,
    )


def resolve_answers(
    question: str,
    answer_list: list[str],
    analysis: str,
    model: Optional[str] = None,
) -> str:
    """Resolve answers by addressing flaws and enhancing strengths.

    Args:
        question: Original question
        answer_list: List of original answers
        analysis: Analysis of the answers
        model: Model to use

    Returns:
        Resolved/improved answers
    """
    print("Resolving Initial Answers Based on Analysis...")
    client = get_client()

    # Format original answers
    formatted_answers = "\n\n".join(
        [f"### Original Answer {i + 1}:\n{answer}" for i, answer in enumerate(answer_list)]
    )

    user_message = f"""\
Please improve the following answers by addressing the identified weaknesses and enhancing the strengths.

## Original Question:
{question}

## Original Answers:
{formatted_answers}

## Analysis:
{analysis}

## Task:
For each answer, provide an improved version that:
1. Addresses the identified flaws and weaknesses
2. Preserves and enhances the identified strengths
3. Ensures logical consistency and completeness

## Format:
Provide each improved answer clearly labeled as "Improved Answer 1", "Improved Answer 2", etc.
"""

    return generate_response(
        client=client,
        system_prompt=RESOLVE_SYSTEM,
        user_message=user_message,
        temperature=0.0,
        model=model,
    )


def select_answer(
    question: str,
    resolved_answers: str,
    model: Optional[str] = None,
) -> str:
    """Select the best answer from resolved answers.

    Args:
        question: Original question
        resolved_answers: Resolved/improved answers
        model: Model to use

    Returns:
        Selected best answer with justification
    """
    print("Selecting Best Answer...")
    client = get_client()

    user_message = f"""\
Please select the best answer from the following improved answers.

## Original Question:
{question}

## Improved Answers:
{resolved_answers}

## Task:
1. Evaluate each improved answer against the criteria of accuracy, completeness, clarity, and practicality
2. Select the single best answer
3. Explain your reasoning for the selection

## Format:
- **Selected Answer**: [Number or identifier of the best answer]
- **Reasoning**: [Why this answer is the best]
- **Full Answer**: [The complete text of the selected answer]
"""

    return generate_response(
        client=client,
        system_prompt=SELECT_SYSTEM,
        user_message=user_message,
        temperature=0.0,
        model=model,
    )


async def run_smartpilot(
    question: str,
    n: int = 3,
    model: Optional[str] = None,
) -> dict[str, any]:
    """Run the complete SmartPilot pipeline.

    Args:
        question: The question to answer
        n: Number of initial answers to generate
        model: Model to use

    Returns:
        Dictionary containing all pipeline outputs
    """
    # Step 1: Generate multiple answers
    print(f"Generating {n} initial answers...")
    answer_list = await generate_multiple_initial_answers(question, n, model)

    # Step 2: Analyze answers
    print("Analyzing answers...")
    analysis = analyze_answers(question, answer_list, model)

    # Step 3: Resolve answers
    resolved_answers = resolve_answers(question, answer_list, analysis, model)

    # Step 4: Select best answer
    selected_answer = select_answer(question, resolved_answers, model)

    return {
        "question": question,
        "initial_answers": answer_list,
        "analysis": analysis,
        "resolved_answers": resolved_answers,
        "selected_answer": selected_answer,
    }


def main() -> None:
    """Main entry point for CLI usage."""
    import sys

    print("=" * 60)
    print("SmartPilot - AI-Powered Question Answering")
    print("=" * 60)
    print()

    question = input("What is your question? ").strip()
    if not question:
        print("Error: Please provide a question.")
        sys.exit(1)

    try:
        n = int(input("How many initial answers to generate? [3]: ").strip() or "3")
        if n < 1 or n > 10:
            print("Number of answers must be between 1 and 10.")
            sys.exit(1)
    except ValueError:
        print("Invalid number. Using default of 3.")
        n = 3

    print()

    try:
        result = asyncio.run(run_smartpilot(question, n))

        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)

        print("\n### Initial Answers Generated:")
        for i, answer in enumerate(result["initial_answers"], 1):
            print(f"\n--- Answer {i} ---")
            print(answer[:500] + "..." if len(answer) > 500 else answer)

        print("\n### Analysis:")
        print(result["analysis"][:1000] + "..." if len(result["analysis"]) > 1000 else result["analysis"])

        print("\n### Resolved Answers:")
        print(
            result["resolved_answers"][:1000] + "..."
            if len(result["resolved_answers"]) > 1000
            else result["resolved_answers"]
        )

        print("\n### Selected Best Answer:")
        print(result["selected_answer"])

    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
