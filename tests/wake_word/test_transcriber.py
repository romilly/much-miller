"""Integration tests for HttpTranscriber."""

import pytest
from hamcrest import assert_that, instance_of

import httpx

from much_miller.wake_word.adapters import HttpTranscriber


def transcriber_available() -> bool:
    """Check if transcriber API is running."""
    try:
        response = httpx.get("http://localhost:8765/", timeout=1.0)
        return response.status_code == 200
    except httpx.RequestError:
        return False


requires_transcriber = pytest.mark.skipif(
    not transcriber_available(),
    reason="Transcriber API not available at localhost:8765"
)


class TestHttpTranscriber:
    """Integration tests for HttpTranscriber."""

    @requires_transcriber
    def test_transcribe_returns_text_from_response(self) -> None:
        transcriber = HttpTranscriber()
        # Minimal valid WAV file (silence)
        wav_bytes = create_silent_wav(duration_seconds=0.5)

        result = transcriber.transcribe(wav_bytes)

        assert_that(result, instance_of(str))

    def test_transcribe_raises_on_http_error(self) -> None:
        transcriber = HttpTranscriber(base_url="http://localhost:9999")
        wav_bytes = create_silent_wav(duration_seconds=0.1)

        with pytest.raises(httpx.RequestError):
            transcriber.transcribe(wav_bytes)


def create_silent_wav(duration_seconds: float, sample_rate: int = 16000) -> bytes:
    """Create a valid WAV file with silence."""
    import io
    import wave
    import numpy as np

    num_samples = int(sample_rate * duration_seconds)
    samples = np.zeros(num_samples, dtype=np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())

    return buffer.getvalue()
