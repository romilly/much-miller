"""BBC Radio player adapter using mpv."""

import subprocess

from much_miller.radio.ports import RadioPlayerPort


class BBCRadioPlayer(RadioPlayerPort):
    """Plays BBC radio streams via mpv."""

    def __init__(self) -> None:
        self._process: subprocess.Popen[bytes] | None = None
        self._current_station: str | None = None

    @property
    def current_station(self) -> str | None:
        """Return the name of the currently playing station, or None."""
        return self._current_station

    def play(self, station_id: str, station_name: str) -> None:
        """Start playing a station.

        Args:
            station_id: The BBC station identifier (e.g., 'bbc_radio_three')
            station_name: Human-readable station name for display
        """
        self.stop()
        url = f"https://lsn.lv/bbcradio.m3u8?station={station_id}&bitrate=320000"
        self._process = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._current_station = station_name

    def stop(self) -> None:
        """Stop playback."""
        if self._process:
            self._process.terminate()
            self._process = None
            self._current_station = None

    def is_playing(self) -> bool:
        """Check if currently playing."""
        return self._process is not None and self._process.poll() is None
