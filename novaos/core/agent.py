"""
NovaOS Core Agent
-----------------
Orchestrates perception, planning, and action execution using a LangGraph
state machine. Every action that touches the desktop goes through a
safety-confirmation gate before execution.
"""

from __future__ import annotations

import json
import logging
import platform
from typing import Any, Dict, List, Optional, TypedDict

import ollama

from novaos.config import config
from novaos.control.keyboard import KeyboardController
from novaos.control.mouse import MouseController
from novaos.memory.vector import MemoryManager
from novaos.vision.screenshot import VisionModule

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LangGraph-compatible state definition
# ---------------------------------------------------------------------------

class AgentState(TypedDict):
    command: str
    context: List[str]
    screen_state: Optional[Dict[str, Any]]
    plan: Optional[str]
    actions: List[Dict[str, Any]]
    result: Optional[str]
    confirmed: bool


# ---------------------------------------------------------------------------
# Action registry
# ---------------------------------------------------------------------------

AVAILABLE_ACTIONS = {
    "move_mouse": "Move the mouse cursor to (x, y).",
    "click": "Click the mouse at (x, y) with a given button.",
    "type_text": "Type a string of text using the keyboard.",
    "press_key": "Press a single keyboard key.",
    "hotkey": "Press a keyboard shortcut (e.g. ctrl+c).",
    "capture_screen": "Take a screenshot and return the file path.",
    "open_app": "Open an application by name.",
    "run_command": "Execute a shell command.",
    "wait": "Wait for a specified number of seconds.",
}


# ---------------------------------------------------------------------------
# Main agent class
# ---------------------------------------------------------------------------

class NovaAgent:
    """
    NovaOS autonomous desktop agent.

    The agent follows a Perceive → Plan → Confirm → Act → Remember loop.
    """

    SYSTEM_PROMPT = (
        "You are NovaOS, an autonomous desktop AI agent running on "
        f"{platform.system()} {platform.release()}. "
        "Your job is to help the user by controlling their computer. "
        "When given a command, respond with a JSON object containing:\n"
        "  - 'plan': a short human-readable explanation of what you will do.\n"
        "  - 'actions': a list of action objects, each with 'type' (one of "
        f"{list(AVAILABLE_ACTIONS.keys())}) and 'params' (a dict of parameters).\n"
        "Always prefer the least intrusive action. Never perform destructive "
        "operations without explicit user confirmation."
    )

    def __init__(self) -> None:
        self.vision = VisionModule()
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.memory = MemoryManager()
        self.model = config.DEFAULT_MODEL

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_command(self, command: str, use_vision: bool = False) -> str:
        """
        Full Perceive → Plan → Confirm → Act → Remember cycle.

        Parameters
        ----------
        command:
            Natural-language instruction from the user.
        use_vision:
            Whether to capture the current screen before planning.

        Returns
        -------
        str
            A human-readable summary of what was done.
        """
        logger.info("Processing command: %s", command)

        # 1. Perceive
        context = self.memory.search(command)
        screen_state: Optional[Dict[str, Any]] = None
        if use_vision or self._needs_vision(command):
            screen_state = self.vision.analyze_screen()

        # 2. Plan
        plan_json = self._plan(command, context, screen_state)

        # 3. Confirm (if safe-mode is on)
        if config.SAFE_MODE and plan_json.get("actions"):
            approved = self._request_confirmation(plan_json)
            if not approved:
                return "Action cancelled by user."

        # 4. Act
        result = self._execute_plan(plan_json)

        # 5. Remember
        summary = plan_json.get("plan", result)
        self.memory.store(command, summary)

        return summary

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _needs_vision(self, command: str) -> bool:
        vision_keywords = {"see", "look", "click", "find", "screen", "window", "open"}
        return bool(vision_keywords.intersection(command.lower().split()))

    def _plan(
        self,
        command: str,
        context: List[str],
        screen_state: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Ask the LLM to produce a structured action plan."""
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        if context:
            messages.append(
                {"role": "system", "content": "Relevant memory:\n" + "\n".join(context)}
            )
        if screen_state:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Current screen text (OCR):\n"
                        + screen_state.get("extracted_text", "")
                    ),
                }
            )
        messages.append({"role": "user", "content": command})

        try:
            response = ollama.chat(model=self.model, messages=messages)
            raw = response["message"]["content"]
            # Try to parse JSON; fall back to plain text plan
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"plan": raw, "actions": []}
        except Exception as exc:
            logger.error("LLM call failed: %s", exc)
            return {"plan": "LLM unavailable.", "actions": []}

    def _request_confirmation(self, plan_json: Dict[str, Any]) -> bool:
        """
        Print the plan and ask for confirmation on the terminal.
        In the full UI this is replaced by a graphical dialog.
        """
        print("\n[NovaOS] Planned actions:")
        print(f"  {plan_json.get('plan', '(no description)')}")
        for i, action in enumerate(plan_json.get("actions", []), 1):
            print(f"  {i}. {action.get('type')} — {action.get('params', {})}")
        answer = input("\nProceed? [y/N] ").strip().lower()
        return answer == "y"

    def _execute_plan(self, plan_json: Dict[str, Any]) -> str:
        """Dispatch each action in the plan to the appropriate controller."""
        results: List[str] = []
        for action in plan_json.get("actions", []):
            action_type = action.get("type", "")
            params = action.get("params", {})
            try:
                result = self._dispatch_action(action_type, params)
                results.append(result)
            except Exception as exc:
                logger.error("Action %s failed: %s", action_type, exc)
                results.append(f"[ERROR] {action_type}: {exc}")
        return "\n".join(results) if results else plan_json.get("plan", "Done.")

    def _dispatch_action(self, action_type: str, params: Dict[str, Any]) -> str:
        if action_type == "move_mouse":
            self.mouse.move_to(params["x"], params["y"])
            return f"Moved mouse to ({params['x']}, {params['y']})"
        elif action_type == "click":
            self.mouse.click(params.get("x"), params.get("y"), params.get("button", "left"))
            return f"Clicked at ({params.get('x')}, {params.get('y')})"
        elif action_type == "type_text":
            self.keyboard.type_text(params["text"])
            return f"Typed: {params['text']}"
        elif action_type == "press_key":
            self.keyboard.press_key(params["key"])
            return f"Pressed key: {params['key']}"
        elif action_type == "hotkey":
            self.keyboard.hotkey(*params["keys"])
            return f"Hotkey: {params['keys']}"
        elif action_type == "capture_screen":
            path = self.vision.capture_screen()
            return f"Screenshot saved: {path}"
        elif action_type == "wait":
            import time
            time.sleep(params.get("seconds", 1))
            return f"Waited {params.get('seconds', 1)}s"
        else:
            return f"Unknown action: {action_type}"
