"""Audio recorder adapter using sounddevice."""

import io
import wave

import numpy as np
import sounddevice as sd

from much_miller.wake_word.ports import AudioRecorderPort


class SoundDeviceRecorder(AudioRecorderPort):
    """Audio recorder that captures from microphone using sounddevice."""

    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate

    def record_chunk(self, duration_seconds: float) -> bytes:
        """Record a chunk of audio from the microphone.

        Args:
            duration_seconds: Duration to record

        Returns:
            WAV-encoded audio bytes
        """
        num_samples = int(self.sample_rate * duration_seconds)
        recording = sd.rec(
            num_samples,
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16,
        )
        sd.wait()

        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(recording.tobytes())

        return buffer.getvalue()
