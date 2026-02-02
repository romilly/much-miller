"""Fake radio player for testing."""

from much_miller.radio.ports import RadioPlayerPort


class FakeRadioPlayer(RadioPlayerPort):
    """Fake radio player for testing - tracks play/stop calls."""

    def __init__(self) -> None:
        self._current_station: str | None = None
        self._playing: bool = False
        self.play_calls: list[tuple[str, str]] = []
        self.stop_calls: int = 0

    @property
    def current_station(self) -> str | None:
        """Return the name of the currently playing station, or None."""
        return self._current_station

    def play(self, station_id: str, station_name: str) -> None:
        """Record play call and update state."""
        self.play_calls.append((station_id, station_name))
        self._current_station = station_name
        self._playing = True

    def stop(self) -> None:
        """Record stop call and update state."""
        self.stop_calls += 1
        self._current_station = None
        self._playing = False

    def is_playing(self) -> bool:
        """Check if currently playing."""
        return self._playing
