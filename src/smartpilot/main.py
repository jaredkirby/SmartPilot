"""SmartPilot main module - AI-powered question answering system using OpenAI Chat Completions API."""

import asyncio
import os
from typing import Any, Callable, Optional

from dotenv import load_dotenv
from openai import OpenAI
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
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

StageReporter = Callable[[str], None]
ProgressCallback = Callable[[int, int], None]


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
    """Generate a response using OpenAI Chat Completions API.

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
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    if assistant_prefix:
        messages.append({"role": "assistant", "content": assistant_prefix})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content


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
    loop = asyncio.get_running_loop()
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
    use_tqdm: bool = True,
    progress_callback: Optional[ProgressCallback] = None,
) -> list[str]:
    """Generate multiple initial answers to a question.

    Args:
        question: The question to answer
        n: Number of answers to generate
        model: Model to use
        use_tqdm: Whether to display a tqdm progress bar
        progress_callback: Optional callback for reporting progress externally

    Returns:
        List of generated answers
    """
    client = get_client()
    answer_list = []

    tasks = [generate_single_answer(client, question, model) for _ in range(n)]

    pbar = tqdm(total=n, desc="Generating answers") if use_tqdm else None

    try:
        for future in asyncio.as_completed(tasks):
            answer = await future
            answer_list.append(answer)

            if progress_callback:
                progress_callback(len(answer_list), n)

            if pbar:
                pbar.update(1)
    finally:
        if pbar:
            pbar.close()

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
    reporter: Optional[StageReporter] = None,
    progress_callback: Optional[ProgressCallback] = None,
) -> dict[str, Any]:
    """Run the complete SmartPilot pipeline.

    Args:
        question: The question to answer
        n: Number of initial answers to generate
        model: Model to use
        reporter: Optional callback for reporting stage updates
        progress_callback: Optional callback for reporting generation progress

    Returns:
        Dictionary containing all pipeline outputs
    """

    def report(stage: str) -> None:
        if reporter:
            reporter(stage)

    report("Generating initial answers")
    answer_list = await generate_multiple_initial_answers(
        question,
        n,
        model,
        use_tqdm=progress_callback is None,
        progress_callback=progress_callback,
    )

    report("Analyzing answers")
    analysis = analyze_answers(question, answer_list, model)

    report("Resolving answers")
    resolved_answers = resolve_answers(question, answer_list, analysis, model)

    report("Selecting best answer")
    selected_answer = select_answer(question, resolved_answers, model)

    return {
        "question": question,
        "initial_answers": answer_list,
        "analysis": analysis,
        "resolved_answers": resolved_answers,
        "selected_answer": selected_answer,
    }


def _render_header(console: Console) -> None:
    """Display a stylized SmartPilot header."""
    console.print(
        Panel.fit(
            "[bold magenta]SmartPilot[/bold magenta]\n[white]AI-powered multi-answer reasoning[/white]",
            border_style="magenta",
        )
    )


def _prompt_user_inputs(console: Console) -> tuple[str, int]:
    """Prompt the user for a question and number of answers."""
    question = Prompt.ask("[bold cyan]What question should SmartPilot tackle?[/]").strip()
    while not question:
        console.print("[red]Please enter a question to continue.[/]")
        question = Prompt.ask("[bold cyan]What question should SmartPilot tackle?[/]").strip()

    attempts = 0
    while True:
        try:
            n = IntPrompt.ask(
                "[bold cyan]How many initial answers should we craft?[/] (1-10)",
                default=3,
            )
            if 1 <= n <= 10:
                return question, n
            console.print("[yellow]Choose a value between 1 and 10.[/]")
        except ValueError:
            attempts += 1
            console.print("[red]Please provide a number.[/]")
            if attempts >= 3:
                console.print("[yellow]Falling back to 3 answers.[/]")
                return question, 3


def _display_results(console: Console, result: dict[str, Any]) -> None:
    """Pretty-print SmartPilot outputs."""
    console.print(
        Panel(
            Markdown(f"**Question**\n\n{result['question']}"),
            border_style="cyan",
            title="Prompt",
        )
    )

    table = Table(
        title="Initial Answers",
        box=box.ROUNDED,
        show_lines=True,
        expand=True,
    )
    table.add_column("Option", style="bold cyan", width=12, no_wrap=True)
    table.add_column("Outline", style="white")

    for idx, answer in enumerate(result["initial_answers"], start=1):
        snippet = answer.strip()
        if len(snippet) > 800:
            snippet = snippet[:800].rstrip() + "..."
        table.add_row(f"Answer {idx}", snippet or "[dim]No content[/dim]")

    console.print(table)

    console.print(
        Panel(
            Markdown(result["analysis"]),
            title="Analysis",
            border_style="yellow",
        )
    )

    console.print(
        Panel(
            Markdown(result["resolved_answers"]),
            title="Resolved Answers",
            border_style="blue",
        )
    )

    console.print(
        Panel(
            Markdown(result["selected_answer"]),
            title="Selected Answer",
            border_style="green",
        )
    )


def main() -> None:
    """Main entry point for CLI usage."""
    import sys

    console = Console()
    _render_header(console)
    question, n = _prompt_user_inputs(console)
    console.print()

    status = console.status("[bold cyan]Preparing SmartPilot...[/]", spinner="dots")
    status.start()

    try:
        with Progress(
            SpinnerColumn(style="magenta"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("{task.completed}/{task.total}", style="cyan"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            progress_task = progress.add_task("[cyan]Generating answers", total=n)
            progress_task_active = True

            def progress_callback(completed: int, total: int) -> None:
                progress.update(progress_task, completed=completed, total=total)

            def reporter(stage: str) -> None:
                nonlocal progress_task_active
                status.update(f"[bold cyan]{stage}[/]")
                console.log(f"[bold cyan]{stage}[/]")
                if progress_task_active and stage != "Generating initial answers":
                    progress.remove_task(progress_task)
                    progress_task_active = False

            result = asyncio.run(
                run_smartpilot(
                    question,
                    n,
                    reporter=reporter,
                    progress_callback=progress_callback,
                )
            )
    except ValueError as exc:
        status.stop()
        console.print(Panel(str(exc), title="Configuration Error", border_style="red"))
        sys.exit(1)
    except Exception as exc:
        status.stop()
        console.print(Panel(str(exc), title="SmartPilot Error", border_style="red"))
        sys.exit(1)

    status.stop()
    console.rule("[bold green]SmartPilot Results")
    _display_results(console, result)


if __name__ == "__main__":
    main()
