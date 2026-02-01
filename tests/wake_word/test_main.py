"""Tests for wake word detection orchestration."""

from hamcrest import assert_that, contains_string, is_

from much_miller.wake_word.adapters import (
    FakeRecorder,
    FakeSpeaker,
    FakeTranscriber,
    FakeVoiceDetector,
)
from much_miller.main import process_audio_chunk


class TestProcessAudioChunk:
    """Tests for the process_audio_chunk function."""

    def test_returns_true_when_wake_word_detected(self) -> None:
        recorder = FakeRecorder(wav_bytes=b"fake wav data")
        transcriber = FakeTranscriber(response="figaro what time is it")

        result = process_audio_chunk(recorder, transcriber)

        assert_that(result, is_(True))

    def test_returns_false_when_no_wake_word(self) -> None:
        recorder = FakeRecorder(wav_bytes=b"fake wav data")
        transcriber = FakeTranscriber(response="hello world")

        result = process_audio_chunk(recorder, transcriber)

        assert_that(result, is_(False))

    def test_says_hello_when_wake_word_detected(self) -> None:
        recorder = FakeRecorder(wav_bytes=b"fake wav data")
        transcriber = FakeTranscriber(response="figaro")
        speaker = FakeSpeaker()

        process_audio_chunk(recorder, transcriber, speaker=speaker)

        assert_that(speaker.spoken_text, contains_string("Hello Romilly"))

    def test_skips_transcription_when_no_speech_detected(self) -> None:
        recorder = FakeRecorder(wav_bytes=b"fake wav data")
        transcriber = FakeTranscriber(response="figaro")  # Would match if called
        voice_detector = FakeVoiceDetector(has_speech=False)

        result = process_audio_chunk(
            recorder, transcriber, voice_detector=voice_detector
        )

        assert_that(result, is_(False))
