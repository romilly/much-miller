"""Tests for speaker adapters."""

from pathlib import Path

import pytest
from hamcrest import assert_that, contains_string, instance_of

from much_miller.wake_word.adapters import FakeSpeaker, PiperSpeaker


class TestFakeSpeaker:
    """Tests for FakeSpeaker adapter."""

    def test_stores_spoken_text(self) -> None:
        speaker = FakeSpeaker()

        speaker.say("Yes?")

        assert_that(speaker.spoken_text, contains_string("Yes?"))


def model_available() -> bool:
    """Check if the voice model is available."""
    model_path = Path(__file__).parent.parent.parent / "models" / "en_GB-alan-medium.onnx"
    return model_path.exists()


requires_model = pytest.mark.skipif(
    not model_available(),
    reason="Voice model not available at models/en_GB-alan-medium.onnx"
)


class TestPiperSpeaker:
    """Integration tests for PiperSpeaker adapter."""

    @requires_model
    def test_can_be_instantiated_with_model_path(self) -> None:
        model_path = Path(__file__).parent.parent.parent / "models" / "en_GB-alan-medium.onnx"

        speaker = PiperSpeaker(model_path=model_path)

        assert_that(speaker, instance_of(PiperSpeaker))
