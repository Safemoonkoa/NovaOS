"""
NovaOS Vision Module
--------------------
Handles screen capture, OCR text extraction, and optional VLM-based
image understanding via Ollama (e.g. LLaVA, Moondream, Qwen2-VL).
"""

from __future__ import annotations

import base64
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import mss
import mss.tools
from PIL import Image

from novaos.config import config

logger = logging.getLogger(__name__)

SCREENSHOT_DIR = Path(os.path.expanduser("~/.novaos/screenshots"))


class VisionModule:
    """Captures the screen and extracts visual information."""

    def __init__(self) -> None:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        self._sct = mss.mss()
        self._ocr_reader = None  # Lazy-loaded

    # ------------------------------------------------------------------
    # Screen capture
    # ------------------------------------------------------------------

    def capture_screen(self, monitor_index: int = 1) -> str:
        """
        Capture the specified monitor and save it as a PNG.

        Returns
        -------
        str
            Absolute path to the saved screenshot.
        """
        monitor = self._sct.monitors[monitor_index]
        output = str(SCREENSHOT_DIR / "current_screen.png")
        sct_img = self._sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        logger.debug("Screenshot saved to %s", output)
        return output

    def capture_region(self, left: int, top: int, width: int, height: int) -> str:
        """Capture a specific region of the screen."""
        region = {"left": left, "top": top, "width": width, "height": height}
        output = str(SCREENSHOT_DIR / "region.png")
        sct_img = self._sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

    # ------------------------------------------------------------------
    # OCR
    # ------------------------------------------------------------------

    def extract_text(self, image_path: str) -> str:
        """Extract text from an image using EasyOCR."""
        reader = self._get_ocr_reader()
        if reader is None:
            return ""
        try:
            result = reader.readtext(image_path)
            return " ".join(item[1] for item in result)
        except Exception as exc:
            logger.error("OCR failed: %s", exc)
            return ""

    def _get_ocr_reader(self):
        if self._ocr_reader is None:
            try:
                import easyocr  # type: ignore
                self._ocr_reader = easyocr.Reader(["en"], gpu=False)
            except ImportError:
                logger.warning("easyocr not installed — OCR disabled.")
        return self._ocr_reader

    # ------------------------------------------------------------------
    # VLM reasoning
    # ------------------------------------------------------------------

    def describe_screen(self, prompt: str = "Describe what you see on the screen.") -> str:
        """
        Send the current screenshot to a local VLM (e.g. LLaVA) via Ollama
        and return its description.
        """
        image_path = self.capture_screen()
        return self.describe_image(image_path, prompt)

    def describe_image(self, image_path: str, prompt: str) -> str:
        """Send an image to the configured vision model via Ollama."""
        try:
            import ollama  # type: ignore
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            response = ollama.chat(
                model=config.VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_data],
                    }
                ],
            )
            return response["message"]["content"]
        except Exception as exc:
            logger.error("VLM call failed: %s", exc)
            return ""

    # ------------------------------------------------------------------
    # Combined analysis
    # ------------------------------------------------------------------

    def analyze_screen(self) -> Dict[str, Any]:
        """
        Capture the screen, run OCR, and optionally run VLM description.

        Returns a dict with 'image_path' and 'extracted_text'.
        """
        image_path = self.capture_screen()
        text = self.extract_text(image_path)
        return {"image_path": image_path, "extracted_text": text}
