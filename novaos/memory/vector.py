import chromadb
import logging
from typing import List, Dict, Any
from novaos.config import config

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name="novaos_memory")
        
    def store(self, command: str, response: str, metadata: Dict[str, Any] = None):
        """Store an interaction in memory."""
        try:
            self.collection.add(
                documents=[f"Command: {command}\nResponse: {response}"],
                metadatas=[metadata or {}],
                ids=[str(hash(command + response))]
            )
            logger.info(f"Stored interaction in memory: {command}")
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
            
    def search(self, query: str, n_results: int = 3) -> List[str]:
        """Search memory for relevant context."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"Failed to search memory: {e}")
            return []
