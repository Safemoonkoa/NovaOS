"""Unit tests for the NovaOS core agent."""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch


class TestNovaAgent:
    """Tests for NovaAgent._needs_vision and _parse_plan."""

    def test_needs_vision_true(self):
        from novaos.core.agent import NovaAgent
        agent = NovaAgent.__new__(NovaAgent)
        assert agent._needs_vision("click on the button") is True
        assert agent._needs_vision("look at the screen") is True
        assert agent._needs_vision("find the icon") is True

    def test_needs_vision_false(self):
        from novaos.core.agent import NovaAgent
        agent = NovaAgent.__new__(NovaAgent)
        assert agent._needs_vision("what time is it") is False
        assert agent._needs_vision("type hello world") is False

    def test_dispatch_wait(self):
        from novaos.core.agent import NovaAgent
        import time
        agent = NovaAgent.__new__(NovaAgent)
        start = time.time()
        result = agent._dispatch_action("wait", {"seconds": 0.1})
        elapsed = time.time() - start
        assert "Waited" in result
        assert elapsed >= 0.1

    def test_dispatch_unknown(self):
        from novaos.core.agent import NovaAgent
        agent = NovaAgent.__new__(NovaAgent)
        result = agent._dispatch_action("unknown_action", {})
        assert "Unknown" in result
