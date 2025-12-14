# SmartPilot

SmartPilot is an AI-powered question answering system that generates, analyzes, and selects the best answer to a given question. It leverages OpenAI's Chat Completions API with GPT-4 Turbo to provide high-quality, reliable, and accurate responses through a multi-step reasoning pipeline.

## Overview

SmartPilot uses a sophisticated pipeline to improve answer quality:

1. **Generate**: Creates multiple initial answers using high-temperature sampling for diversity
2. **Analyze**: Evaluates each answer's strengths, weaknesses, and logical consistency
3. **Resolve**: Improves answers by addressing identified flaws and enhancing strengths
4. **Select**: Chooses the best final answer based on accuracy, completeness, and clarity

## Installation

This project uses [UV](https://github.com/astral-sh/uv) for modern Python package management.

### Using UV (Recommended)

```bash
# Install UV if not already installed
pip install uv

# Install the project and dependencies
uv sync

# Install with development dependencies (for testing)
uv sync --extra dev

# Install with Streamlit support
uv sync --extra streamlit
```

### Using pip

```bash
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# With Streamlit support
pip install -e ".[streamlit]"
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Command Line Interface

```bash
# Using UV
uv run python -m smartpilot.main

# Or using the installed package
smartpilot
```

You will be prompted to enter your question and the number of initial answers to generate.

### Streamlit Web Interface

```bash
# Using UV
uv run streamlit run src/smartpilot/streamlit_app.py

# Or using the installed package
streamlit run src/smartpilot/streamlit_app.py
```

### As a Python Library

```python
import asyncio
from smartpilot.main import run_smartpilot

async def main():
    result = await run_smartpilot(
        question="What is the best way to learn Python?",
        n=3  # Number of initial answers to generate
    )
    
    print("Best Answer:", result["selected_answer"])

asyncio.run(main())
```

## Development

### Running Tests

```bash
# Using UV
uv run pytest

# With verbose output
uv run pytest -v

# Using pytest directly
pytest tests/
```

### Project Structure

```
smartpilot/
├── src/
│   └── smartpilot/
│       ├── __init__.py
│       ├── main.py          # Core pipeline logic
│       ├── prompts.py       # System prompts
│       └── streamlit_app.py # Web interface
├── tests/
│   ├── test_main.py
│   └── test_prompts.py
├── pyproject.toml           # Project configuration
└── README.md
```

## Credits

This program was inspired by the ideas discussed in the [AI Explained YouTube Channel's video on SmartGPT](https://youtu.be/wVzuvf9D9BU).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
