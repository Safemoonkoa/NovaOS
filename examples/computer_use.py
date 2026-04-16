"""
NovaOS Example: Computer Use Mode
----------------------------------
Demonstrates how NovaOS can control the desktop step-by-step
using vision and the mouse/keyboard controllers.
"""

from novaos.core.agent import NovaAgent

def main():
    agent = NovaAgent()
    
    # This command will trigger vision + desktop control
    task = (
        "Open Chrome, navigate to https://finance.yahoo.com, "
        "search for NVIDIA stock price, and take a screenshot."
    )
    
    print(f"[Task] {task}")
    result = agent.process_command(task, use_vision=True)
    print(f"[Result] {result}")

if __name__ == "__main__":
    main()
