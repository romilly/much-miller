"""Tests for speaker adapters."""

from hamcrest import assert_that, contains_string

from much_miller.wake_word.adapters import FakeSpeaker


class TestFakeSpeaker:
    """Tests for FakeSpeaker adapter."""

    def test_stores_spoken_text(self) -> None:
        speaker = FakeSpeaker()

        speaker.say("Yes?")

        assert_that(speaker.spoken_text, contains_string("Yes?"))
