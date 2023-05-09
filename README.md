# SmartPilot

SmartPilot is a Python program that generates, analyzes, and selects the best answer to a given question. It leverages the power of OpenAI's language model and a series of prompt-engineered AI models to provide high-quality, reliable, and accurate responses.

## Overview

SmartPilot consists of several steps:

1.  Generate multiple initial answers to a question
2.  Analyze the strengths and weaknesses of each answer
3.  Resolve each answer by addressing its flaws and enhancing its strengths
4.  Select the best answer from the resolved answers

## Installation

To install the required packages for SmartPilot, run the following command:
`pip install -r requirements.txt`

## Usage

To use SmartPilot, run `main.py` in your terminal:
`python main.py`

You will be prompted to enter your question and the number of initial answers you want. After providing the necessary input, the program will generate answers, analyze them, resolve them, and finally select the best answer.

## Credits

This program was inspired by the ideas discussed in the AI Explained YouTube Channel's video on SmartGPT(https://youtu.be/wVzuvf9D9BU)

Also uses [LangChain](https://github.com/hwchase17/langchain), a Python library for chaining together multiple language models.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/LICENSE) file for details.
