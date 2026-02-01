"""Piper TTS speaker adapter."""

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import sounddevice as sd
from piper import PiperVoice

from much_miller.wake_word.ports import SpeakerPort

if TYPE_CHECKING:
    from numpy.typing import NDArray


class PiperSpeaker(SpeakerPort):
    """Speaker adapter using Piper TTS."""

    def __init__(self, model_path: Path) -> None:
        """Initialize the Piper speaker.

        Args:
            model_path: Path to the ONNX voice model file
        """
        self._voice = PiperVoice.load(str(model_path))

    def say(self, text: str) -> None:
        """Speak the given text using Piper TTS.

        Args:
            text: Text to speak
        """
        audio_segments: list[NDArray[np.int16]] = []
        for chunk in self._voice.synthesize(text):
            audio_segment = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            audio_segments.append(audio_segment)

        if audio_segments:
            audio_data = np.concatenate(audio_segments)
            sd.play(audio_data, samplerate=self._voice.config.sample_rate)
            sd.wait()
