"""
NovaOS VLM Utilities
--------------------
Higher-level helpers for visual question answering and element detection
using local vision-language models (LLaVA, Moondream, Qwen2-VL, etc.).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from novaos.config import config
from novaos.vision.screenshot import VisionModule

logger = logging.getLogger(__name__)


class VLMReasoner:
    """Wraps the VisionModule with task-specific reasoning prompts."""

    def __init__(self) -> None:
        self.vision = VisionModule()

    def find_element(self, description: str) -> Optional[Dict[str, Any]]:
        """
        Ask the VLM to locate a UI element on the current screen.

        Returns a dict with estimated 'x', 'y' coordinates, or None.
        """
        prompt = (
            f"Look at this screenshot. Find the UI element described as: '{description}'. "
            "Return ONLY a JSON object with keys 'x' and 'y' representing the center "
            "pixel coordinates of that element. If not found, return null."
        )
        raw = self.vision.describe_screen(prompt)
        try:
            import json
            data = json.loads(raw)
            return data
        except Exception:
            logger.warning("VLM did not return valid coordinates for: %s", description)
            return None

    def answer_question(self, question: str) -> str:
        """Ask the VLM a free-form question about the current screen."""
        return self.vision.describe_screen(question)

    def list_visible_apps(self) -> List[str]:
        """Return a list of application names visible on the current screen."""
        prompt = (
            "Look at this screenshot. List all visible application windows or "
            "taskbar icons. Return ONLY a JSON array of application names."
        )
        raw = self.vision.describe_screen(prompt)
        try:
            import json
            return json.loads(raw)
        except Exception:
            return []
