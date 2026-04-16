"""
NovaOS Skill: Browser
---------------------
Opens URLs and performs basic web navigation using the system default browser.
"""

from __future__ import annotations

import logging
import webbrowser
from urllib.parse import quote_plus

from novaos.skills import BaseSkill, register

logger = logging.getLogger(__name__)


class BrowserSkill(BaseSkill):
    name = "skill_browser"
    description = "Open URLs, search the web, and navigate pages."
    version = "0.1.0"

    def run(self, action: str = "open", url: str = "", query: str = "") -> str:
        """
        Parameters
        ----------
        action:
            'open' to open a URL, 'search' to perform a web search.
        url:
            URL to open (used when action='open').
        query:
            Search query (used when action='search').
        """
        if action == "search":
            url = f"https://www.google.com/search?q={quote_plus(query)}"
        if url:
            webbrowser.open(url)
            logger.info("Opened URL: %s", url)
            return f"Opened: {url}"
        return "No URL or query provided."


# Auto-register
register(BrowserSkill())
