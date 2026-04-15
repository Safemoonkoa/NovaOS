import pyautogui
import logging
from novaos.config import config

logger = logging.getLogger(__name__)

class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.require_confirmation = config.REQUIRE_CONFIRMATION
        
    def move_to(self, x: int, y: int, duration: float = 0.5):
        """Move the mouse to specific coordinates."""
        if self._confirm_action(f"Move mouse to ({x}, {y})"):
            pyautogui.moveTo(x, y, duration=duration)
            logger.info(f"Moved mouse to ({x}, {y})")
            
    def click(self, x: int = None, y: int = None, button: str = 'left'):
        """Click the mouse at current or specific coordinates."""
        if self._confirm_action(f"Click {button} button at ({x}, {y})"):
            if x is not None and y is not None:
                pyautogui.click(x=x, y=y, button=button)
            else:
                pyautogui.click(button=button)
            logger.info(f"Clicked {button} button")
            
    def _confirm_action(self, action: str) -> bool:
        if not self.require_confirmation:
            return True
        # In a real app, this would prompt the user via UI
        logger.warning(f"Action requires confirmation: {action}")
        return True # Mocked for MVP
