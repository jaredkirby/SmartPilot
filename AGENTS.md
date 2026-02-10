# Repository Guidelines

## Project Structure & Module Organization
SmartPilot uses a src-layout: `src/smartpilot` contains `main.py` for the pipeline, `prompts.py` for system prompts, and `streamlit_app.py` for the optional UI. Project metadata sits in `pyproject.toml`, and `tests/` holds mirrored suites such as `test_main.py` and `test_prompts.py`. Add fixtures or assets beside the feature they support so imports remain predictable.

## Build, Test, and Development Commands
- `uv sync --extra dev` – install the package plus dev/test dependencies.
- `uv run python -m smartpilot.main` – launch the CLI pipeline locally.
- `uv run streamlit run src/smartpilot/streamlit_app.py` – start the Streamlit UI for demos.
- `uv run pytest` – execute the full asynchronous test suite.
- `smartpilot` – run the published console script once installed.

## Coding Style & Naming Conventions
Write Python 3.10+ with 4-space indents, type hints, and docstrings patterned after `main.py`. Favor `async` coroutines for OpenAI calls, stream batch progress with `tqdm`, and keep helpers small and composable. Use snake_case for identifiers, PascalCase for classes, and uppercase snake case for prompt constants. Stick to local imports and run your formatter/linter before opening a PR.

## Testing Guidelines
Tests rely on `pytest` and `pytest-asyncio`, so name suites `test_*.py` and decorate coroutine cases with `pytest.mark.asyncio`. Mock OpenAI responses; CI must not call the live API. Add regression tests whenever you edit prompts or pipeline stages, keep analyzer/selector coverage with table-driven inputs, and share the `uv run pytest` (or `-k` filtered) output inside your PR.

## Commit & Pull Request Guidelines
Mirror the imperative, sub-60-character subjects used in `git log` (e.g., “Fix OpenAI API to use Chat Completions API”). Each commit should cover one concern, referencing issues when available. Pull requests need a summary, validation notes (tests, CLI runs, Streamlit checks), any config migrations, and screenshots for UI tweaks. Keep secrets such as `OPENAI_API_KEY` in your environment, not in tracked files.

## Security & Configuration Tips
Export `OPENAI_API_KEY` or store it in `.env`; never commit real keys. Review `pyproject.toml` before adding dependencies and prefer extras (like `streamlit`) for optional stacks. Future provider hooks or logging should be controlled by config flags so the CLI runs without extra setup.
