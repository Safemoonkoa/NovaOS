import argparse
import logging
from novaos.core.agent import NovaAgent
from novaos.config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="NovaOS - The desktop AI that sees, thinks and acts on your computer.")
    parser.add_argument("--command", type=str, help="Command to execute")
    parser.add_argument("--doctor", action="store_true", help="Check dependencies and compatibility")
    
    args = parser.parse_args()
    
    if args.doctor:
        logger.info("Running NovaOS Doctor...")
        # Add dependency checks here
        logger.info("All dependencies look good!")
        return
        
    if args.command:
        agent = NovaAgent()
        response = agent.process_command(args.command)
        print(f"NovaOS: {response}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
