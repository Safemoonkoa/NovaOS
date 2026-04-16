"""
NovaOS Skill: Terminal
----------------------
Execute shell commands safely with output capture and timeout.
"""

from __future__ import annotations

import logging
import subprocess
from typing import Optional

from novaos.config import config
from novaos.skills import BaseSkill, register

logger = logging.getLogger(__name__)

# Commands that are always blocked regardless of safe-mode
BLOCKED_COMMANDS = {"rm -rf /", "mkfs", "dd if=", ":(){:|:&};:"}


class TerminalSkill(BaseSkill):
    name = "skill_terminal"
    description = "Execute shell commands and return their output."
    version = "0.1.0"

    def run(
        self,
        command: str = "",
        timeout: int = 30,
        shell: bool = True,
    ) -> str:
        if not command:
            return "No command provided."
        if self._is_blocked(command):
            return f"Blocked: '{command}' is not allowed for safety reasons."
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout.strip()
            if result.returncode != 0:
                output += f"\n[stderr] {result.stderr.strip()}"
            logger.info("Ran command: %s (exit %d)", command, result.returncode)
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout}s."
        except Exception as exc:
            return f"Error: {exc}"

    def _is_blocked(self, command: str) -> bool:
        for blocked in BLOCKED_COMMANDS:
            if blocked in command:
                return True
        return False


register(TerminalSkill())
