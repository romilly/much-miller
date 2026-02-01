"""HTTP adapter for speech-to-text transcription."""

import httpx

from much_miller.wake_word.ports import TranscriberPort


class HttpTranscriber(TranscriberPort):
    """Transcriber that uses HTTP API for speech-to-text."""

    def __init__(self, base_url: str = "http://localhost:8765") -> None:
        self.base_url = base_url

    def transcribe(self, audio_wav: bytes) -> str:
        """Transcribe audio data to text via HTTP API.

        Args:
            audio_wav: WAV-encoded audio bytes

        Returns:
            Transcribed text

        Raises:
            httpx.RequestError: If the HTTP request fails
        """
        response = httpx.post(
            f"{self.base_url}/api/transcribe",
            content=audio_wav,
            headers={"Content-Type": "audio/wav"},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["text"]
