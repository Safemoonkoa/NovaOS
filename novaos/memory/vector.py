"""
NovaOS Vector Memory
--------------------
Persistent semantic memory backed by ChromaDB. Stores command/response pairs
and retrieves the most relevant context for new queries.
"""

from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import chromadb

from novaos.config import config

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages long-term semantic memory for the NovaOS agent."""

    COLLECTION_NAME = "novaos_memory"

    def __init__(self) -> None:
        db_dir = os.path.expanduser(config.CHROMA_DB_DIR)
        os.makedirs(db_dir, exist_ok=True)
        self._client = chromadb.PersistentClient(path=db_dir)
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def store(
        self,
        command: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Persist a command/response pair.

        Parameters
        ----------
        command:
            The user's original instruction.
        response:
            The agent's response or action summary.
        metadata:
            Optional key/value metadata to attach to the record.
        """
        doc = f"Command: {command}\nResponse: {response}"
        doc_id = hashlib.md5(doc.encode()).hexdigest()
        meta = metadata or {}
        meta["timestamp"] = datetime.utcnow().isoformat()
        meta["command"] = command[:200]

        try:
            self._collection.upsert(
                documents=[doc],
                metadatas=[meta],
                ids=[doc_id],
            )
            logger.debug("Stored memory: %s", command[:60])
        except Exception as exc:
            logger.error("Failed to store memory: %s", exc)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def search(self, query: str, n_results: int = 3) -> List[str]:
        """
        Retrieve the most semantically similar stored interactions.

        Parameters
        ----------
        query:
            The search query (usually the current user command).
        n_results:
            Maximum number of results to return.

        Returns
        -------
        List[str]
            List of relevant document strings.
        """
        try:
            count = self._collection.count()
            if count == 0:
                return []
            results = self._collection.query(
                query_texts=[query],
                n_results=min(n_results, count),
            )
            return results["documents"][0] if results["documents"] else []
        except Exception as exc:
            logger.error("Memory search failed: %s", exc)
            return []

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recently stored interactions."""
        try:
            results = self._collection.get(
                limit=limit,
                include=["documents", "metadatas"],
            )
            items = []
            for doc, meta in zip(results["documents"], results["metadatas"]):
                items.append({"document": doc, "metadata": meta})
            return sorted(items, key=lambda x: x["metadata"].get("timestamp", ""), reverse=True)
        except Exception as exc:
            logger.error("get_recent failed: %s", exc)
            return []

    def clear(self) -> None:
        """Delete all stored memories."""
        try:
            self._client.delete_collection(self.COLLECTION_NAME)
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("Memory cleared.")
        except Exception as exc:
            logger.error("Failed to clear memory: %s", exc)
