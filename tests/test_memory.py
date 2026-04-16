"""Unit tests for the NovaOS memory module."""

from __future__ import annotations

import os
import tempfile
import pytest

from novaos.memory.vector import MemoryManager


@pytest.fixture
def memory(tmp_path, monkeypatch):
    monkeypatch.setenv("CHROMA_DB_DIR", str(tmp_path / "memory"))
    from novaos import config as cfg_module
    cfg_module.config.CHROMA_DB_DIR = str(tmp_path / "memory")
    return MemoryManager()


class TestMemoryManager:
    def test_store_and_search(self, memory):
        memory.store("open chrome", "Opened Chrome browser.")
        results = memory.search("open chrome")
        assert len(results) > 0
        assert "chrome" in results[0].lower()

    def test_search_empty(self, memory):
        results = memory.search("nothing here")
        assert results == []

    def test_clear(self, memory):
        memory.store("test command", "test response")
        memory.clear()
        results = memory.search("test command")
        assert results == []
