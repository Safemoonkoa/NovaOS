import logging
from typing import Dict, Any, List
import ollama
from novaos.config import config
from novaos.vision.screenshot import VisionModule
from novaos.control.mouse import MouseController
from novaos.control.keyboard import KeyboardController
from novaos.memory.vector import MemoryManager

logger = logging.getLogger(__name__)

class NovaAgent:
    def __init__(self):
        self.vision = VisionModule()
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.memory = MemoryManager()
        self.model = config.DEFAULT_MODEL
        
    def process_command(self, command: str) -> str:
        """Process a user command and execute actions."""
        logger.info(f"Processing command: {command}")
        
        # 1. Retrieve context from memory
        context = self.memory.search(command)
        
        # 2. Capture current screen state if needed
        screen_state = None
        if "see" in command.lower() or "look" in command.lower() or "click" in command.lower():
            screen_state = self.vision.analyze_screen()
            
        # 3. Plan actions using LLM
        prompt = self._build_prompt(command, context, screen_state)
        response = self._call_llm(prompt)
        
        # 4. Execute planned actions (mocked for MVP)
        self._execute_plan(response)
        
        # 5. Store interaction in memory
        self.memory.store(command, response)
        
        return response
        
    def _build_prompt(self, command: str, context: List[str], screen_state: Dict[str, Any] = None) -> str:
        prompt = f"User Command: {command}\n"
        if context:
            prompt += f"Context: {' | '.join(context)}\n"
        if screen_state:
            prompt += f"Screen State: {screen_state}\n"
        prompt += "Plan the necessary actions to fulfill the command."
        return prompt
        
    def _call_llm(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': 'You are NovaOS, an autonomous desktop AI agent.'},
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "I encountered an error while thinking."
            
    def _execute_plan(self, plan: str):
        # Parse plan and execute actions (e.g., mouse clicks, typing)
        # This is a simplified version for the MVP
        logger.info(f"Executing plan: {plan}")
        pass
