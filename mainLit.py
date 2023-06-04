import streamlit as st
import asyncio
from main import (
    generate_multiple_initial_answers,
    analyze_answers,
    resolve_answers,
    select_answer,
)


# This decorator means that this function will run every time a button
# or input field is changed and the page is rerendered
@st.cache_data
def run_smart_pilot(question, n):
    # Generate 'n' answers to the question
    answer_list = asyncio.run(generate_multiple_initial_answers(question, n))

    # Analyze all answers
    analysis = analyze_answers(question, answer_list)

    # Resolve answers using analysis from analyze_answers()
    resolved_answers = resolve_answers(question, analysis)

    # Select the best answer from the resolved answers
    selected_answer = select_answer(question, resolved_answers)

    return answer_list, analysis, resolved_answers, selected_answer


def main():
    st.title("SmartPilot")
    st.write("Welcome to the SmartPilot system.")

    prewritten_questions = [
        "Question 1",
        "Question 2",
        "Question 3",
    ]  # List of prewritten questions
    question_input_method = st.radio(
        "Select method to input question:",
        ("Type a question", "Choose a prewritten question"),
    )

    if question_input_method == "Type a question":
        question = st.text_input("What is your question?")
    else:
        question = st.selectbox("Select a prewritten question:", prewritten_questions)

    n = st.number_input(
        "How many answers do you want?", min_value=1, max_value=10, value=1, step=1
    )

    if st.button("Run SmartPilot"):
        if question:
            st.write("Processing... Please wait...")
            answer_list, analysis, resolved_answers, selected_answer = run_smart_pilot(
                question, n
            )

            st.markdown("### Generated Answers:")
            st.markdown(answer_list)

            st.markdown("### Analysis of Answers:")
            st.markdown(analysis)

            st.markdown("### Resolved Answers:")
            st.markdown(resolved_answers)

            st.markdown("### Selected Best Answer:")
            st.markdown(selected_answer)

        else:
            st.warning("Please input a question.")


if __name__ == "__main__":
    main()
