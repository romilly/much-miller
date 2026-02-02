"""Abstract base class for radio player."""

from abc import ABC, abstractmethod


class RadioPlayerPort(ABC):
    """Abstract base class for radio playback services."""

    @property
    @abstractmethod
    def current_station(self) -> str | None:
        """Return the name of the currently playing station, or None."""

    @abstractmethod
    def play(self, station_id: str, station_name: str) -> None:
        """Start playing a station.

        Args:
            station_id: The station identifier for the stream URL
            station_name: Human-readable station name for display
        """

    @abstractmethod
    def stop(self) -> None:
        """Stop playback."""

    @abstractmethod
    def is_playing(self) -> bool:
        """Check if currently playing."""
