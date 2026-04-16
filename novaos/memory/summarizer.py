"""
NovaOS Conversation Summarizer
-------------------------------
Periodically compresses long conversation histories into concise summaries
to keep the LLM context window manageable.
"""

from __future__ import annotations

import logging
from typing import List

import ollama

from novaos.config import config

logger = logging.getLogger(__name__)

SUMMARIZE_PROMPT = (
    "Summarize the following conversation history into a concise paragraph "
    "that captures the key facts, user preferences, and completed tasks. "
    "Focus on information that will be useful for future interactions."
)


class ConversationSummarizer:
    """Compresses conversation history using the local LLM."""

    def __init__(self) -> None:
        self.model = config.DEFAULT_MODEL

    def summarize(self, history: List[str]) -> str:
        """
        Summarize a list of conversation turns.

        Parameters
        ----------
        history:
            List of strings, each representing a command/response pair.

        Returns
        -------
        str
            A concise summary of the conversation.
        """
        if not history:
            return ""
        combined = "\n\n".join(history)
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SUMMARIZE_PROMPT},
                    {"role": "user", "content": combined},
                ],
            )
            return response["message"]["content"]
        except Exception as exc:
            logger.error("Summarization failed: %s", exc)
            return combined[:500]
