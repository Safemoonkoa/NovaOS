"""
NovaOS Task Planner
-------------------
Breaks complex, multi-step tasks into an ordered list of sub-goals using
chain-of-thought prompting. Each sub-goal is then handed off to the main
agent for execution.
"""

from __future__ import annotations

import logging
from typing import List

import ollama

from novaos.config import config

logger = logging.getLogger(__name__)

PLANNER_SYSTEM_PROMPT = (
    "You are a task-planning assistant for NovaOS. "
    "Given a high-level goal, decompose it into an ordered list of concrete, "
    "atomic sub-tasks that a desktop automation agent can execute one by one. "
    "Return ONLY a numbered list, one sub-task per line. "
    "Be specific and actionable."
)


class TaskPlanner:
    """Decomposes high-level goals into executable sub-tasks."""

    def __init__(self) -> None:
        self.model = config.DEFAULT_MODEL

    def decompose(self, goal: str) -> List[str]:
        """
        Decompose a goal into a list of sub-tasks.

        Parameters
        ----------
        goal:
            High-level natural-language goal.

        Returns
        -------
        List[str]
            Ordered list of sub-task descriptions.
        """
        logger.info("Decomposing goal: %s", goal)
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                    {"role": "user", "content": goal},
                ],
            )
            raw = response["message"]["content"]
            return self._parse_steps(raw)
        except Exception as exc:
            logger.error("Planner LLM call failed: %s", exc)
            return [goal]

    @staticmethod
    def _parse_steps(raw: str) -> List[str]:
        steps: List[str] = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip leading numbering like "1." or "1)"
            if line[0].isdigit():
                line = line.lstrip("0123456789.)- ").strip()
            if line:
                steps.append(line)
        return steps
