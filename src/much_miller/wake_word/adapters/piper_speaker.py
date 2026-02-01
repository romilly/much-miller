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
        audio_arrays: list[NDArray[np.float32]] = []
        for chunk in self._voice.synthesize(text):
            audio_arrays.append(chunk.audio_float_array)

        if audio_arrays:
            audio_data = np.concatenate(audio_arrays)
            sd.play(audio_data, samplerate=self._voice.config.sample_rate)
            sd.wait()
