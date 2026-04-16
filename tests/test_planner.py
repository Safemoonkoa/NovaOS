"""Unit tests for the NovaOS task planner."""

from __future__ import annotations

from novaos.core.planner import TaskPlanner


class TestTaskPlanner:
    def test_parse_steps_numbered(self):
        raw = "1. Open Chrome\n2. Navigate to google.com\n3. Search for NVIDIA"
        steps = TaskPlanner._parse_steps(raw)
        assert len(steps) == 3
        assert steps[0] == "Open Chrome"
        assert steps[2] == "Search for NVIDIA"

    def test_parse_steps_empty(self):
        steps = TaskPlanner._parse_steps("")
        assert steps == []

    def test_parse_steps_no_numbers(self):
        raw = "Open Chrome\nNavigate to google.com"
        steps = TaskPlanner._parse_steps(raw)
        assert len(steps) == 2
