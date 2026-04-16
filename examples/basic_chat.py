"""
NovaOS Example: Basic Chat
--------------------------
Demonstrates how to use the NovaAgent programmatically.
"""

from novaos.core.agent import NovaAgent

def main():
    agent = NovaAgent()
    
    commands = [
        "What is the current time?",
        "List the files in my home directory",
        "Open a web browser and go to https://github.com",
    ]
    
    for cmd in commands:
        print(f"\n[You] {cmd}")
        response = agent.process_command(cmd)
        print(f"[NovaOS] {response}")

if __name__ == "__main__":
    main()
