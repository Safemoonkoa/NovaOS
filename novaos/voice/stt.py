"""
NovaOS Speech-to-Text
---------------------
Transcribes audio using faster-whisper (local, no cloud required).
Falls back to the standard openai-whisper library if faster-whisper
is not available.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechToText:
    """Local speech recognition powered by Whisper."""

    def __init__(self, model_size: str = "base") -> None:
        self.model_size = model_size
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model
        try:
            from faster_whisper import WhisperModel  # type: ignore
            self._model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            logger.info("Loaded faster-whisper model: %s", self.model_size)
        except ImportError:
            try:
                import whisper  # type: ignore
                self._model = whisper.load_model(self.model_size)
                logger.info("Loaded openai-whisper model: %s", self.model_size)
            except ImportError:
                logger.error("Neither faster-whisper nor openai-whisper is installed.")
                self._model = None
        return self._model

    def transcribe_file(self, audio_path: str) -> str:
        """
        Transcribe an audio file to text.

        Parameters
        ----------
        audio_path:
            Path to an audio file (.wav, .mp3, .m4a, etc.).

        Returns
        -------
        str
            Transcribed text, or empty string on failure.
        """
        model = self._load_model()
        if model is None:
            return ""
        try:
            # faster-whisper API
            if hasattr(model, "transcribe") and "faster" in str(type(model).__module__):
                segments, _ = model.transcribe(audio_path, beam_size=5)
                return " ".join(seg.text for seg in segments).strip()
            else:
                # openai-whisper API
                result = model.transcribe(audio_path)
                return result["text"].strip()
        except Exception as exc:
            logger.error("Transcription failed: %s", exc)
            return ""

    def transcribe_microphone(self, duration: float = 5.0) -> str:
        """
        Record from the microphone for `duration` seconds and transcribe.

        Requires sounddevice and scipy to be installed.
        """
        try:
            import sounddevice as sd  # type: ignore
            import scipy.io.wavfile as wav  # type: ignore
            import numpy as np

            logger.info("Recording for %.1f seconds...", duration)
            sample_rate = 16000
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
            )
            sd.wait()

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp_path = f.name
            wav.write(tmp_path, sample_rate, recording)
            text = self.transcribe_file(tmp_path)
            os.unlink(tmp_path)
            return text
        except ImportError:
            logger.error("sounddevice or scipy not installed — cannot record from microphone.")
            return ""
        except Exception as exc:
            logger.error("Microphone recording failed: %s", exc)
            return ""
