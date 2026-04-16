"""Unit tests for NovaOS skills."""

from __future__ import annotations

import os
import tempfile

from novaos.skills.skill_files import FilesSkill
from novaos.skills.skill_terminal import TerminalSkill


class TestFilesSkill:
    def test_list(self, tmp_path):
        skill = FilesSkill()
        (tmp_path / "hello.txt").write_text("hi")
        result = skill.run(action="list", path=str(tmp_path))
        assert "hello.txt" in result

    def test_read_write(self, tmp_path):
        skill = FilesSkill()
        path = str(tmp_path / "test.txt")
        skill.run(action="write", path=path, content="NovaOS rocks!")
        content = skill.run(action="read", path=path)
        assert content == "NovaOS rocks!"

    def test_delete(self, tmp_path):
        skill = FilesSkill()
        path = str(tmp_path / "del.txt")
        skill.run(action="write", path=path, content="delete me")
        skill.run(action="delete", path=path)
        assert not os.path.exists(path)


class TestTerminalSkill:
    def test_echo(self):
        skill = TerminalSkill()
        result = skill.run(command="echo NovaOS")
        assert "NovaOS" in result

    def test_blocked_command(self):
        skill = TerminalSkill()
        result = skill.run(command="rm -rf /")
        assert "Blocked" in result
