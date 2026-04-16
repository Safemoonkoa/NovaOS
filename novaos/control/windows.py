"""
NovaOS Window Manager
---------------------
Cross-platform window management utilities. Uses platform-specific backends:
  - Windows: pywinauto
  - macOS:   pyobjc / AppKit
  - Linux:   xdotool via subprocess
"""

from __future__ import annotations

import logging
import platform
import subprocess
from typing import List, Optional

logger = logging.getLogger(__name__)

OS = platform.system()


class WindowManager:
    """Lists, focuses, and manipulates application windows."""

    def list_windows(self) -> List[str]:
        """Return a list of visible window titles."""
        if OS == "Windows":
            return self._list_windows_win()
        elif OS == "Darwin":
            return self._list_windows_mac()
        else:
            return self._list_windows_linux()

    def focus_window(self, title: str) -> bool:
        """Bring a window with the given title to the foreground."""
        if OS == "Windows":
            return self._focus_win(title)
        elif OS == "Darwin":
            return self._focus_mac(title)
        else:
            return self._focus_linux(title)

    def open_app(self, app_name: str) -> bool:
        """Open an application by name."""
        try:
            if OS == "Windows":
                subprocess.Popen(["start", app_name], shell=True)
            elif OS == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
            logger.info("Opened app: %s", app_name)
            return True
        except Exception as exc:
            logger.error("Failed to open %s: %s", app_name, exc)
            return False

    # ------------------------------------------------------------------
    # Platform-specific implementations
    # ------------------------------------------------------------------

    def _list_windows_win(self) -> List[str]:
        try:
            import pywinauto  # type: ignore
            from pywinauto import Desktop
            return [w.window_text() for w in Desktop(backend="uia").windows()]
        except ImportError:
            logger.warning("pywinauto not installed.")
            return []

    def _list_windows_mac(self) -> List[str]:
        try:
            from AppKit import NSWorkspace  # type: ignore
            apps = NSWorkspace.sharedWorkspace().runningApplications()
            return [a.localizedName() for a in apps if a.activationPolicy() == 0]
        except ImportError:
            logger.warning("pyobjc not installed.")
            return []

    def _list_windows_linux(self) -> List[str]:
        try:
            result = subprocess.run(
                ["xdotool", "search", "--name", ""],
                capture_output=True, text=True
            )
            return result.stdout.strip().splitlines()
        except FileNotFoundError:
            logger.warning("xdotool not installed.")
            return []

    def _focus_win(self, title: str) -> bool:
        try:
            import pywinauto  # type: ignore
            from pywinauto import Desktop
            win = Desktop(backend="uia").window(title_re=f".*{title}.*")
            win.set_focus()
            return True
        except Exception as exc:
            logger.error("focus_win failed: %s", exc)
            return False

    def _focus_mac(self, title: str) -> bool:
        script = f'tell application "{title}" to activate'
        try:
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except Exception as exc:
            logger.error("focus_mac failed: %s", exc)
            return False

    def _focus_linux(self, title: str) -> bool:
        try:
            subprocess.run(["xdotool", "search", "--name", title, "windowactivate"], check=True)
            return True
        except Exception as exc:
            logger.error("focus_linux failed: %s", exc)
            return False
