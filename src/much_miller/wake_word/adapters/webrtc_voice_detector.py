"""WebRTC VAD voice detector adapter."""

import io
import wave

import webrtcvad

from much_miller.wake_word.ports import VoiceDetectorPort


class WebRtcVoiceDetector(VoiceDetectorPort):
    """Voice detector using WebRTC VAD."""

    def __init__(self, aggressiveness: int = 2, speech_threshold: float = 0.3) -> None:
        """Initialize the voice detector.

        Args:
            aggressiveness: VAD aggressiveness (0-3), higher = more aggressive filtering
            speech_threshold: Fraction of frames that must contain speech (0.0-1.0)
        """
        self._vad = webrtcvad.Vad(aggressiveness)
        self._speech_threshold = speech_threshold

    def contains_speech(self, audio_wav: bytes) -> bool:
        """Check if audio contains speech.

        Args:
            audio_wav: WAV-encoded audio bytes

        Returns:
            True if speech detected, False otherwise
        """
        sample_rate, audio_data = self._parse_wav(audio_wav)
        frames = self._split_into_frames(audio_data, sample_rate)

        if not frames:
            return False

        speech_frames = sum(
            1 for frame in frames if self._vad.is_speech(frame, sample_rate)
        )
        speech_ratio = speech_frames / len(frames)
        return speech_ratio >= self._speech_threshold

    def _parse_wav(self, audio_wav: bytes) -> tuple[int, bytes]:
        """Parse WAV file and return sample rate and raw audio data."""
        with wave.open(io.BytesIO(audio_wav), "rb") as wav_file:
            sample_rate = wav_file.getframerate()
            audio_data = wav_file.readframes(wav_file.getnframes())
        return sample_rate, audio_data

    def _split_into_frames(
        self, audio_data: bytes, sample_rate: int, frame_duration_ms: int = 30
    ) -> list[bytes]:
        """Split audio into frames suitable for VAD.

        Args:
            audio_data: Raw 16-bit audio bytes
            sample_rate: Sample rate in Hz
            frame_duration_ms: Frame duration (10, 20, or 30 ms)

        Returns:
            List of audio frames
        """
        frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # 2 bytes per sample
        frames = []
        for i in range(0, len(audio_data) - frame_size + 1, frame_size):
            frames.append(audio_data[i : i + frame_size])
        return frames
