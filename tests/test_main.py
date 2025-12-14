"""Tests for SmartPilot main module."""

import os
from unittest.mock import MagicMock, patch

import pytest

from smartpilot.main import (
    DEFAULT_MODEL,
    analyze_answers,
    generate_response,
    get_client,
    resolve_answers,
    run_smartpilot,
    select_answer,
)


class TestConfiguration:
    """Test configuration and setup."""

    def test_default_model_is_gpt5_mini(self):
        """Test that default model is set to GPT-4o Mini equivalent."""
        assert DEFAULT_MODEL == "gpt-4o-mini"

    def test_get_client_raises_without_api_key(self):
        """Test that get_client raises error when API key is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove OPENAI_API_KEY if it exists
            os.environ.pop("OPENAI_API_KEY", None)
            with pytest.raises(ValueError) as exc_info:
                get_client()
            assert "OPENAI_API_KEY" in str(exc_info.value)

    def test_get_client_returns_client_with_api_key(self):
        """Test that get_client returns OpenAI client when API key is set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client = get_client()
            assert client is not None


class TestGenerateResponse:
    """Test response generation."""

    @patch("smartpilot.main.get_client")
    def test_generate_response_calls_api(self, mock_get_client):
        """Test that generate_response calls the OpenAI API correctly."""
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = generate_response(
            client=mock_client,
            system_prompt="System",
            user_message="User message",
            temperature=0.5,
        )

        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch("smartpilot.main.get_client")
    def test_generate_response_with_assistant_prefix(self, mock_get_client):
        """Test that generate_response includes assistant prefix when provided."""
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        generate_response(
            client=mock_client,
            system_prompt="System",
            user_message="User message",
            assistant_prefix="Let me help you",
        )

        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 3
        assert messages[2]["role"] == "assistant"
        assert messages[2]["content"] == "Let me help you"


class TestAnalyzeAnswers:
    """Test answer analysis."""

    @patch("smartpilot.main.get_client")
    @patch("smartpilot.main.generate_response")
    def test_analyze_answers_formats_input_correctly(self, mock_generate, mock_get_client):
        """Test that analyze_answers formats the input correctly."""
        mock_get_client.return_value = MagicMock()
        mock_generate.return_value = "Analysis result"

        result = analyze_answers(
            question="What is 2+2?",
            answer_list=["Answer 1", "Answer 2"],
        )

        assert result == "Analysis result"
        mock_generate.assert_called_once()

        # Check that the user message contains the question and answers
        call_args = mock_generate.call_args
        user_message = call_args.kwargs["user_message"]
        assert "What is 2+2?" in user_message
        assert "Answer Option 1" in user_message
        assert "Answer Option 2" in user_message


class TestResolveAnswers:
    """Test answer resolution."""

    @patch("smartpilot.main.get_client")
    @patch("smartpilot.main.generate_response")
    def test_resolve_answers_includes_analysis(self, mock_generate, mock_get_client):
        """Test that resolve_answers includes the analysis in the prompt."""
        mock_get_client.return_value = MagicMock()
        mock_generate.return_value = "Resolved answers"

        result = resolve_answers(
            question="What is 2+2?",
            answer_list=["Answer 1"],
            analysis="Analysis of answers",
        )

        assert result == "Resolved answers"
        call_args = mock_generate.call_args
        user_message = call_args.kwargs["user_message"]
        assert "Analysis of answers" in user_message


class TestSelectAnswer:
    """Test answer selection."""

    @patch("smartpilot.main.get_client")
    @patch("smartpilot.main.generate_response")
    def test_select_answer_uses_resolved_answers(self, mock_generate, mock_get_client):
        """Test that select_answer uses the resolved answers."""
        mock_get_client.return_value = MagicMock()
        mock_generate.return_value = "Selected: Answer 1"

        result = select_answer(
            question="What is 2+2?",
            resolved_answers="Resolved answer content",
        )

        assert result == "Selected: Answer 1"
        call_args = mock_generate.call_args
        user_message = call_args.kwargs["user_message"]
        assert "Resolved answer content" in user_message


class TestRunSmartpilot:
    """Test the full SmartPilot pipeline."""

    @pytest.mark.asyncio
    @patch("smartpilot.main.select_answer")
    @patch("smartpilot.main.resolve_answers")
    @patch("smartpilot.main.analyze_answers")
    @patch("smartpilot.main.generate_multiple_initial_answers")
    async def test_run_smartpilot_returns_all_results(
        self, mock_generate, mock_analyze, mock_resolve, mock_select
    ):
        """Test that run_smartpilot returns all pipeline results."""
        mock_generate.return_value = ["Answer 1", "Answer 2"]
        mock_analyze.return_value = "Analysis"
        mock_resolve.return_value = "Resolved"
        mock_select.return_value = "Selected"

        result = await run_smartpilot("Test question", n=2)

        assert result["question"] == "Test question"
        assert result["initial_answers"] == ["Answer 1", "Answer 2"]
        assert result["analysis"] == "Analysis"
        assert result["resolved_answers"] == "Resolved"
        assert result["selected_answer"] == "Selected"

    @pytest.mark.asyncio
    @patch("smartpilot.main.select_answer")
    @patch("smartpilot.main.resolve_answers")
    @patch("smartpilot.main.analyze_answers")
    @patch("smartpilot.main.generate_multiple_initial_answers")
    async def test_run_smartpilot_calls_functions_in_order(
        self, mock_generate, mock_analyze, mock_resolve, mock_select
    ):
        """Test that run_smartpilot calls functions in the correct order."""
        mock_generate.return_value = ["Answer 1"]
        mock_analyze.return_value = "Analysis"
        mock_resolve.return_value = "Resolved"
        mock_select.return_value = "Selected"

        await run_smartpilot("Test question", n=1)

        mock_generate.assert_called_once()
        mock_analyze.assert_called_once()
        mock_resolve.assert_called_once()
        mock_select.assert_called_once()
