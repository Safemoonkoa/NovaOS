"""
NovaOS Text-to-Speech
---------------------
Synthesizes speech locally using Piper TTS, with edge-tts as a fallback
for systems that prefer a lighter dependency footprint.
"""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Local TTS engine with automatic backend selection."""

    def __init__(self, voice: str = "en_US-lessac-medium") -> None:
        self.voice = voice
        self._backend: str = self._detect_backend()

    def _detect_backend(self) -> str:
        try:
            subprocess.run(["piper", "--version"], capture_output=True, check=True)
            return "piper"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        try:
            import edge_tts  # type: ignore
            return "edge_tts"
        except ImportError:
            pass
        logger.warning("No TTS backend found. Speech output disabled.")
        return "none"

    def speak(self, text: str) -> None:
        """Synthesize and play `text` using the available TTS backend."""
        if self._backend == "piper":
            self._speak_piper(text)
        elif self._backend == "edge_tts":
            self._speak_edge_tts(text)
        else:
            logger.warning("TTS disabled — cannot speak: %s", text[:60])

    def synthesize_to_file(self, text: str, output_path: str) -> bool:
        """Save synthesized speech to a WAV/MP3 file."""
        if self._backend == "piper":
            return self._piper_to_file(text, output_path)
        elif self._backend == "edge_tts":
            return self._edge_tts_to_file(text, output_path)
        return False

    # ------------------------------------------------------------------
    # Piper backend
    # ------------------------------------------------------------------

    def _speak_piper(self, text: str) -> None:
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp = f.name
            self._piper_to_file(text, tmp)
            subprocess.run(["aplay", tmp], check=True)
            os.unlink(tmp)
        except Exception as exc:
            logger.error("Piper TTS failed: %s", exc)

    def _piper_to_file(self, text: str, output_path: str) -> bool:
        try:
            proc = subprocess.run(
                ["piper", "--model", self.voice, "--output_file", output_path],
                input=text.encode(),
                capture_output=True,
            )
            return proc.returncode == 0
        except Exception as exc:
            logger.error("Piper synthesis failed: %s", exc)
            return False

    # ------------------------------------------------------------------
    # edge-tts backend
    # ------------------------------------------------------------------

    def _speak_edge_tts(self, text: str) -> None:
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp = f.name
            self._edge_tts_to_file(text, tmp)
            subprocess.run(["mpg123", tmp], check=True)
            os.unlink(tmp)
        except Exception as exc:
            logger.error("edge-tts playback failed: %s", exc)

    def _edge_tts_to_file(self, text: str, output_path: str) -> bool:
        try:
            import edge_tts  # type: ignore
            async def _run():
                communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
                await communicate.save(output_path)
            asyncio.run(_run())
            return True
        except Exception as exc:
            logger.error("edge-tts synthesis failed: %s", exc)
            return False
