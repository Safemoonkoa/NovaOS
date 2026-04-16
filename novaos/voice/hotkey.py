"""
NovaOS Global Hotkey Listener
------------------------------
Listens for the global hotkey (default: Ctrl+Alt+N) and triggers
hands-free voice input via the SpeechToText module.
"""

from __future__ import annotations

import logging
import threading
from typing import Callable, Optional

from pynput import keyboard  # type: ignore

logger = logging.getLogger(__name__)

DEFAULT_HOTKEY = "<ctrl>+<alt>+n"


class HotkeyListener:
    """Registers a global hotkey and calls a callback when triggered."""

    def __init__(
        self,
        callback: Callable[[], None],
        hotkey: str = DEFAULT_HOTKEY,
    ) -> None:
        self.callback = callback
        self.hotkey = hotkey
        self._listener: Optional[keyboard.GlobalHotKeys] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start listening for the hotkey in a background thread."""
        self._listener = keyboard.GlobalHotKeys({self.hotkey: self._on_activate})
        self._thread = threading.Thread(target=self._listener.start, daemon=True)
        self._thread.start()
        logger.info("Hotkey listener started: %s", self.hotkey)

    def stop(self) -> None:
        """Stop the hotkey listener."""
        if self._listener:
            self._listener.stop()
        logger.info("Hotkey listener stopped.")

    def _on_activate(self) -> None:
        logger.info("Hotkey activated: %s", self.hotkey)
        threading.Thread(target=self.callback, daemon=True).start()
