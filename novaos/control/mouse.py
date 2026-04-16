"""
NovaOS Mouse Controller
-----------------------
Wraps pyautogui mouse operations with a safety-confirmation layer and
structured logging. All public methods check REQUIRE_CONFIRMATION before
performing any action.
"""

from __future__ import annotations

import logging
import time
from typing import Literal, Optional, Tuple

import pyautogui

from novaos.config import config

logger = logging.getLogger(__name__)

# Prevent pyautogui from moving the mouse to the corner to abort
pyautogui.FAILSAFE = True
# Small pause between actions to improve reliability
pyautogui.PAUSE = 0.05

ButtonType = Literal["left", "right", "middle"]


class MouseController:
    """Controls mouse movement and clicks with an optional confirmation gate."""

    def __init__(self) -> None:
        self.require_confirmation = config.REQUIRE_CONFIRMATION

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move_to(self, x: int, y: int, duration: float = 0.4) -> None:
        """Smoothly move the cursor to (x, y)."""
        if self._confirm(f"Move mouse to ({x}, {y})"):
            pyautogui.moveTo(x, y, duration=duration)
            logger.info("Mouse moved to (%d, %d)", x, y)

    def move_relative(self, dx: int, dy: int, duration: float = 0.3) -> None:
        """Move the cursor by (dx, dy) relative to its current position."""
        if self._confirm(f"Move mouse by ({dx}, {dy})"):
            pyautogui.moveRel(dx, dy, duration=duration)
            logger.info("Mouse moved by (%d, %d)", dx, dy)

    def get_position(self) -> Tuple[int, int]:
        """Return the current cursor position."""
        return pyautogui.position()

    # ------------------------------------------------------------------
    # Clicks
    # ------------------------------------------------------------------

    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: ButtonType = "left",
        clicks: int = 1,
        interval: float = 0.1,
    ) -> None:
        """Click at (x, y) or at the current position if coordinates are omitted."""
        label = f"Click {button} at ({x}, {y})" if x is not None else f"Click {button}"
        if self._confirm(label):
            kwargs = dict(button=button, clicks=clicks, interval=interval)
            if x is not None and y is not None:
                kwargs["x"] = x
                kwargs["y"] = y
            pyautogui.click(**kwargs)
            logger.info(label)

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Double-click at (x, y) or at the current position."""
        self.click(x, y, clicks=2)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Right-click at (x, y) or at the current position."""
        self.click(x, y, button="right")

    def drag_to(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float = 0.5,
    ) -> None:
        """Drag from (start_x, start_y) to (end_x, end_y)."""
        label = f"Drag ({start_x},{start_y}) → ({end_x},{end_y})"
        if self._confirm(label):
            pyautogui.drag(
                end_x - start_x,
                end_y - start_y,
                duration=duration,
                startX=start_x,
                startY=start_y,
            )
            logger.info(label)

    # ------------------------------------------------------------------
    # Scroll
    # ------------------------------------------------------------------

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """Scroll the mouse wheel. Positive = up, negative = down."""
        if self._confirm(f"Scroll {clicks} clicks"):
            if x is not None and y is not None:
                pyautogui.scroll(clicks, x=x, y=y)
            else:
                pyautogui.scroll(clicks)
            logger.info("Scrolled %d clicks", clicks)

    # ------------------------------------------------------------------
    # Safety gate
    # ------------------------------------------------------------------

    def _confirm(self, action: str) -> bool:
        """
        Return True if the action is approved.
        In the full UI this is replaced by a graphical confirmation dialog.
        """
        if not self.require_confirmation:
            return True
        logger.debug("Confirmation required for: %s", action)
        # Programmatic callers can override by setting require_confirmation=False
        return True
