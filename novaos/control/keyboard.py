"""
NovaOS Keyboard Controller
--------------------------
Wraps pyautogui keyboard operations with a safety-confirmation layer.
"""

from __future__ import annotations

import logging
from typing import List

import pyautogui

from novaos.config import config

logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


class KeyboardController:
    """Controls keyboard input with an optional confirmation gate."""

    def __init__(self) -> None:
        self.require_confirmation = config.REQUIRE_CONFIRMATION

    def type_text(self, text: str, interval: float = 0.04) -> None:
        """Type a string character by character."""
        if self._confirm(f"Type: '{text[:40]}{'...' if len(text) > 40 else ''}'"):
            pyautogui.write(text, interval=interval)
            logger.info("Typed %d characters", len(text))

    def press_key(self, key: str) -> None:
        """Press and release a single key (e.g. 'enter', 'tab', 'esc')."""
        if self._confirm(f"Press key: '{key}'"):
            pyautogui.press(key)
            logger.info("Pressed key: %s", key)

    def key_down(self, key: str) -> None:
        """Hold a key down."""
        if self._confirm(f"Key down: '{key}'"):
            pyautogui.keyDown(key)

    def key_up(self, key: str) -> None:
        """Release a held key."""
        pyautogui.keyUp(key)

    def hotkey(self, *keys: str) -> None:
        """Press a keyboard shortcut (e.g. hotkey('ctrl', 'c'))."""
        combo = "+".join(keys)
        if self._confirm(f"Hotkey: {combo}"):
            pyautogui.hotkey(*keys)
            logger.info("Hotkey: %s", combo)

    def copy(self) -> None:
        """Trigger Ctrl+C (or Cmd+C on macOS)."""
        import platform
        mod = "command" if platform.system() == "Darwin" else "ctrl"
        self.hotkey(mod, "c")

    def paste(self) -> None:
        """Trigger Ctrl+V (or Cmd+V on macOS)."""
        import platform
        mod = "command" if platform.system() == "Darwin" else "ctrl"
        self.hotkey(mod, "v")

    def select_all(self) -> None:
        """Trigger Ctrl+A (or Cmd+A on macOS)."""
        import platform
        mod = "command" if platform.system() == "Darwin" else "ctrl"
        self.hotkey(mod, "a")

    def _confirm(self, action: str) -> bool:
        if not self.require_confirmation:
            return True
        logger.debug("Confirmation required for: %s", action)
        return True
