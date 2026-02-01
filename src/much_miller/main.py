#!/usr/bin/env python3
"""Wake word detection orchestration."""

from much_miller.wake_word.detector import contains_wake_word
from much_miller.wake_word.ports import AudioRecorderPort, SpeakerPort, TranscriberPort


def process_audio_chunk(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
    duration_seconds: float = 2.0,
    speaker: SpeakerPort | None = None,
) -> bool:
    """Record audio, transcribe it, and check for wake word.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
        duration_seconds: Duration to record
        speaker: Optional speaker for TTS response

    Returns:
        True if wake word detected, False otherwise
    """
    audio = recorder.record_chunk(duration_seconds)
    text = transcriber.transcribe(audio)
    if text:
        print(f"Heard: '{text}'")
    detected = contains_wake_word(text)
    if detected and speaker is not None:
        speaker.say("Yes?")
    return detected


def run(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
    speaker: SpeakerPort | None = None,
) -> None:
    """Run the wake word detection loop.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
        speaker: Optional speaker for TTS response
    """
    print("Listening for 'figaro'...")
    try:
        while True:
            if process_audio_chunk(recorder, transcriber, speaker=speaker):
                print("Wake word detected!")
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    from pathlib import Path

    from much_miller.wake_word.adapters import (
        HttpTranscriber,
        PiperSpeaker,
        SoundDeviceRecorder,
    )

    model_path = Path(__file__).parent.parent.parent / "models" / "en_GB-alan-medium.onnx"
    recorder = SoundDeviceRecorder(device=1)
    transcriber = HttpTranscriber()
    speaker = PiperSpeaker(model_path=model_path)
    run(recorder, transcriber, speaker=speaker)
