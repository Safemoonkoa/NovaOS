import pyautogui
import logging
from novaos.config import config

logger = logging.getLogger(__name__)

class KeyboardController:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.require_confirmation = config.REQUIRE_CONFIRMATION
        
    def type_text(self, text: str, interval: float = 0.05):
        """Type a string of text."""
        if self._confirm_action(f"Type text: '{text}'"):
            pyautogui.write(text, interval=interval)
            logger.info(f"Typed text: '{text}'")
            
    def press_key(self, key: str):
        """Press a specific key."""
        if self._confirm_action(f"Press key: '{key}'"):
            pyautogui.press(key)
            logger.info(f"Pressed key: '{key}'")
            
    def hotkey(self, *keys):
        """Press a combination of keys."""
        if self._confirm_action(f"Press hotkey: {keys}"):
            pyautogui.hotkey(*keys)
            logger.info(f"Pressed hotkey: {keys}")
            
    def _confirm_action(self, action: str) -> bool:
        if not self.require_confirmation:
            return True
        # In a real app, this would prompt the user via UI
        logger.warning(f"Action requires confirmation: {action}")
        return True # Mocked for MVP
