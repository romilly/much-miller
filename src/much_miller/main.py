#!/usr/bin/env python3
"""Wake word detection orchestration."""

from much_miller.wake_word.detector import contains_wake_word
from much_miller.wake_word.ports import (
    AudioRecorderPort,
    SpeakerPort,
    TranscriberPort,
    VoiceDetectorPort,
)


def process_audio_chunk(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
    duration_seconds: float = 2.0,
    speaker: SpeakerPort | None = None,
    voice_detector: VoiceDetectorPort | None = None,
) -> bool:
    """Record audio, transcribe it, and check for wake word.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
        duration_seconds: Duration to record
        speaker: Optional speaker for TTS response
        voice_detector: Optional VAD to skip silent audio

    Returns:
        True if wake word detected, False otherwise
    """
    audio = recorder.record_chunk(duration_seconds)

    # Skip transcription if no speech detected
    if voice_detector is not None and not voice_detector.contains_speech(audio):
        return False

    text = transcriber.transcribe(audio)
    if text:
        print(f"Heard: '{text}'")
    detected = contains_wake_word(text)
    if detected and speaker is not None:
        speaker.say("Hello Romilly")
    return detected


def run(
    recorder: AudioRecorderPort,
    transcriber: TranscriberPort,
    speaker: SpeakerPort | None = None,
    voice_detector: VoiceDetectorPort | None = None,
    duration_seconds: float = 2.0,
) -> None:
    """Run the wake word detection loop.

    Args:
        recorder: Audio recorder adapter
        transcriber: Speech-to-text transcriber adapter
        speaker: Optional speaker for TTS response
        voice_detector: Optional VAD to skip silent audio
        duration_seconds: Duration of each audio chunk to record
    """
    print("Listening for 'figaro'...")
    try:
        while True:
            if process_audio_chunk(
                recorder,
                transcriber,
                duration_seconds=duration_seconds,
                speaker=speaker,
                voice_detector=voice_detector,
            ):
                print("Wake word detected!")
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    from much_miller.wake_word.adapters import (
        HttpTranscriber,
        PiperSpeaker,
        SoundDeviceRecorder,
        WebRtcVoiceDetector,
    )

    load_dotenv()
    model_path = Path(os.environ["MUCH_MILLER_MODEL_PATH"])
    transcriber_url = os.environ.get("MUCH_MILLER_TRANSCRIBER_URL", "http://localhost:8765")
    record_duration = float(os.environ.get("MUCH_MILLER_RECORD_DURATION", "2.0"))
    vad_aggressiveness = int(os.environ.get("MUCH_MILLER_VAD_AGGRESSIVENESS", "2"))
    vad_speech_threshold = float(os.environ.get("MUCH_MILLER_VAD_SPEECH_THRESHOLD", "0.3"))
    recorder = SoundDeviceRecorder(device=1)
    transcriber = HttpTranscriber(base_url=transcriber_url)
    speaker = PiperSpeaker(model_path=model_path)
    voice_detector = WebRtcVoiceDetector(
        aggressiveness=vad_aggressiveness,
        speech_threshold=vad_speech_threshold,
    )
    run(
        recorder,
        transcriber,
        speaker=speaker,
        voice_detector=voice_detector,
        duration_seconds=record_duration,
    )
