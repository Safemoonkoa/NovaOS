"""NovaOS Skills — plug-and-play capability modules."""

from __future__ import annotations

import importlib
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

_REGISTRY: Dict[str, "BaseSkill"] = {}


def register(skill: "BaseSkill") -> None:
    _REGISTRY[skill.name] = skill
    logger.info("Skill registered: %s", skill.name)


def get(name: str) -> Optional["BaseSkill"]:
    return _REGISTRY.get(name)


def list_skills():
    return list(_REGISTRY.keys())


class BaseSkill:
    """Base class for all NovaOS skills."""

    name: str = "base"
    description: str = ""
    version: str = "0.1.0"

    def run(self, **kwargs) -> str:
        raise NotImplementedError
