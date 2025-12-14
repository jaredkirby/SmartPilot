"""SmartPilot Streamlit interface."""

import asyncio

import streamlit as st

from smartpilot.main import run_smartpilot


def run_async(coro):
    """Run async function in streamlit context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running event loop
        return asyncio.run(coro)
    else:
        return loop.run_until_complete(coro)


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="SmartPilot",
        page_icon="🧠",
        layout="wide",
    )

    st.title("🧠 SmartPilot")
    st.write("AI-powered question answering with answer generation, analysis, and selection.")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        n = st.slider(
            "Number of initial answers",
            min_value=1,
            max_value=10,
            value=3,
            help="More answers provide better diversity but take longer",
        )

        st.markdown("---")
        st.markdown("### How it works")
        st.markdown("""
        1. **Generate**: Creates multiple initial answers
        2. **Analyze**: Evaluates strengths and weaknesses
        3. **Resolve**: Improves answers based on analysis
        4. **Select**: Chooses the best final answer
        """)

    # Main content
    question = st.text_area(
        "Enter your question:",
        placeholder="What is your question? Be as specific as possible for better results.",
        height=100,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        run_button = st.button("🚀 Run SmartPilot", type="primary", use_container_width=True)

    if run_button:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Processing your question..."):
            try:
                result = run_async(run_smartpilot(question.strip(), n))

                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🎯 Best Answer",
                    "📝 Initial Answers",
                    "🔍 Analysis",
                    "✨ Improved Answers",
                ])

                with tab1:
                    st.markdown("### Selected Best Answer")
                    st.markdown(result["selected_answer"])

                with tab2:
                    st.markdown("### Generated Initial Answers")
                    for i, answer in enumerate(result["initial_answers"], 1):
                        with st.expander(f"Answer {i}", expanded=i == 1):
                            st.markdown(answer)

                with tab3:
                    st.markdown("### Answer Analysis")
                    st.markdown(result["analysis"])

                with tab4:
                    st.markdown("### Improved/Resolved Answers")
                    st.markdown(result["resolved_answers"])

            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
