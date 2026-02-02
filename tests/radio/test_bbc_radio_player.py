"""Tests for BBCRadioPlayer adapter."""

import shutil

import pytest
from hamcrest import assert_that, is_, none

from much_miller.radio.adapters.bbc_radio_player import BBCRadioPlayer


@pytest.fixture
def player() -> BBCRadioPlayer:
    return BBCRadioPlayer()


@pytest.mark.skipif(
    shutil.which("mpv") is None,
    reason="mpv not installed",
)
class TestBBCRadioPlayer:
    """Integration tests for BBCRadioPlayer - requires mpv."""

    def test_initially_not_playing(self, player: BBCRadioPlayer) -> None:
        assert_that(player.is_playing(), is_(False))
        assert_that(player.current_station, is_(none()))

    def test_play_starts_playback(self, player: BBCRadioPlayer) -> None:
        player.play("bbc_radio_three", "radio 3")

        assert_that(player.is_playing(), is_(True))
        assert_that(player.current_station, is_("radio 3"))

        player.stop()

    def test_stop_ends_playback(self, player: BBCRadioPlayer) -> None:
        player.play("bbc_radio_three", "radio 3")
        player.stop()

        assert_that(player.is_playing(), is_(False))
        assert_that(player.current_station, is_(none()))

    def test_play_different_station_stops_previous(
        self, player: BBCRadioPlayer
    ) -> None:
        player.play("bbc_radio_three", "radio 3")
        player.play("bbc_radio_fourfm", "radio 4")

        assert_that(player.current_station, is_("radio 4"))

        player.stop()
