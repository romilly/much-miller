"""Wake word detection orchestration."""

from much_miller.wake_word.detector import contains_wake_word
from much_miller.wake_word.ports import AudioRecorderPort, TranscriberPort


def process_audio_chunk(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
    duration_seconds: float = 2.0,
) -> bool:
    """Record audio, transcribe it, and check for wake word.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
        duration_seconds: Duration to record

    Returns:
        True if wake word detected, False otherwise
    """
    audio = recorder.record_chunk(duration_seconds)
    text = transcriber.transcribe(audio)
    return contains_wake_word(text)


def run(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
) -> None:
    """Run the wake word detection loop.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
    """
    print("Listening for 'hey much'...")
    try:
        while True:
            if process_audio_chunk(recorder, transcriber):
                print("Wake word detected!")
    except KeyboardInterrupt:
        print("\nStopping.")
