import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2")
    VISION_MODEL = os.getenv("VISION_MODEL", "llava:13b")
    
    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", os.path.expanduser("~/.novaos/memory"))
    
    REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
    SAFE_MODE = os.getenv("SAFE_MODE", "true").lower() == "true"
    
    THEME = os.getenv("THEME", "dark")
    ACCENT_COLOR = os.getenv("ACCENT_COLOR", "cyan")

config = Config()
