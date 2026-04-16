"""
NovaOS Skill: Files
-------------------
File system operations: read, write, list, move, copy, delete.
"""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from typing import List

from novaos.skills import BaseSkill, register

logger = logging.getLogger(__name__)


class FilesSkill(BaseSkill):
    name = "skill_files"
    description = "Read, write, list, move, copy, and delete files."
    version = "0.1.0"

    def run(
        self,
        action: str = "list",
        path: str = ".",
        destination: str = "",
        content: str = "",
    ) -> str:
        path = os.path.expanduser(path)
        if action == "list":
            return self._list(path)
        elif action == "read":
            return self._read(path)
        elif action == "write":
            return self._write(path, content)
        elif action == "copy":
            return self._copy(path, destination)
        elif action == "move":
            return self._move(path, destination)
        elif action == "delete":
            return self._delete(path)
        return f"Unknown action: {action}"

    def _list(self, path: str) -> str:
        try:
            entries = os.listdir(path)
            return "\n".join(entries)
        except Exception as exc:
            return f"Error listing {path}: {exc}"

    def _read(self, path: str) -> str:
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as exc:
            return f"Error reading {path}: {exc}"

    def _write(self, path: str, content: str) -> str:
        try:
            Path(path).write_text(content, encoding="utf-8")
            return f"Written: {path}"
        except Exception as exc:
            return f"Error writing {path}: {exc}"

    def _copy(self, src: str, dst: str) -> str:
        try:
            shutil.copy2(src, dst)
            return f"Copied {src} → {dst}"
        except Exception as exc:
            return f"Error copying: {exc}"

    def _move(self, src: str, dst: str) -> str:
        try:
            shutil.move(src, dst)
            return f"Moved {src} → {dst}"
        except Exception as exc:
            return f"Error moving: {exc}"

    def _delete(self, path: str) -> str:
        try:
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(path)
            else:
                p.unlink()
            return f"Deleted: {path}"
        except Exception as exc:
            return f"Error deleting {path}: {exc}"


register(FilesSkill())
