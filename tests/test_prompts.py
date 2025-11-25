"""Tests for SmartPilot prompts module."""

import pytest

from smartpilot.prompts import (
    ANALYZE_SYSTEM,
    ANSWER_ASSISTANT_PREFIX,
    ANSWER_SYSTEM,
    RESOLVE_SYSTEM,
    SELECT_SYSTEM,
)


class TestPrompts:
    """Test suite for prompts module."""

    def test_answer_system_prompt_exists(self):
        """Test that ANSWER_SYSTEM prompt is defined and non-empty."""
        assert ANSWER_SYSTEM
        assert len(ANSWER_SYSTEM) > 50
        assert "step-by-step" in ANSWER_SYSTEM.lower() or "step by step" in ANSWER_SYSTEM.lower()

    def test_answer_assistant_prefix_exists(self):
        """Test that ANSWER_ASSISTANT_PREFIX is defined."""
        assert ANSWER_ASSISTANT_PREFIX
        assert "step" in ANSWER_ASSISTANT_PREFIX.lower()

    def test_analyze_system_prompt_exists(self):
        """Test that ANALYZE_SYSTEM prompt is defined and contains key instructions."""
        assert ANALYZE_SYSTEM
        assert len(ANALYZE_SYSTEM) > 50
        assert "strength" in ANALYZE_SYSTEM.lower()
        assert "weakness" in ANALYZE_SYSTEM.lower() or "flaw" in ANALYZE_SYSTEM.lower()

    def test_resolve_system_prompt_exists(self):
        """Test that RESOLVE_SYSTEM prompt is defined and contains key instructions."""
        assert RESOLVE_SYSTEM
        assert len(RESOLVE_SYSTEM) > 50
        assert "improve" in RESOLVE_SYSTEM.lower() or "address" in RESOLVE_SYSTEM.lower()

    def test_select_system_prompt_exists(self):
        """Test that SELECT_SYSTEM prompt is defined and contains key instructions."""
        assert SELECT_SYSTEM
        assert len(SELECT_SYSTEM) > 50
        assert "select" in SELECT_SYSTEM.lower() or "best" in SELECT_SYSTEM.lower()

    def test_all_prompts_are_strings(self):
        """Test that all prompts are string types."""
        prompts = [
            ANSWER_SYSTEM,
            ANSWER_ASSISTANT_PREFIX,
            ANALYZE_SYSTEM,
            RESOLVE_SYSTEM,
            SELECT_SYSTEM,
        ]
        for prompt in prompts:
            assert isinstance(prompt, str)

    def test_prompts_have_proper_formatting(self):
        """Test that prompts don't have leading/trailing issues."""
        prompts = [
            ANSWER_SYSTEM,
            ANSWER_ASSISTANT_PREFIX,
            ANALYZE_SYSTEM,
            RESOLVE_SYSTEM,
            SELECT_SYSTEM,
        ]
        for prompt in prompts:
            # Should not have excessive whitespace
            assert prompt == prompt.strip() or prompt.endswith("\n")
            # Should not have double newlines at start
            assert not prompt.startswith("\n\n")
