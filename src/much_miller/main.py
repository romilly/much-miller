#!/usr/bin/env python3
"""Much Miller - Local AI assistant with speech interface.

Flow:
1. Listen for wake word (using openWakeWord)
2. Say "Hello Romilly" via TTS
3. Switch to transcription mode (RealtimeSTT)
4. Print transcriptions
5. When transcription ends with "over", return to wake word listening
"""

import os
import sys
from pathlib import Path

# Suppress JACK warnings
os.environ["JACK_NO_START_SERVER"] = "1"

import numpy as np
import pyaudio
import sounddevice as sd
from dotenv import load_dotenv
from openwakeword.model import Model as WakeWordModel
from RealtimeSTT import AudioToTextRecorder

from much_miller.wake_word.adapters import PiperSpeaker
from much_miller.wake_word.ports import SpeakerPort

CHUNK = 1280  # 80ms at 16kHz for openWakeWord
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAKE_WORD_THRESHOLD = 0.5
END_KEYWORD = "over"


def find_device_by_name(name: str) -> int | None:
    """Find audio device index by partial name match (case-insensitive)."""
    for i, dev in enumerate(sd.query_devices()):
        if name.lower() in dev["name"].lower() and dev["max_input_channels"] > 0:
            return i
    return None


def list_input_devices() -> None:
    """List available input devices."""
    print("Available input devices:\n")
    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0:
            print(f"  [{i}] {dev['name']}")
    print()


def listen_for_wake_word(
    device_index: int,
    wake_model: WakeWordModel,
) -> str:
    """Listen for wake word and return which one was detected."""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=CHUNK,
    )

    detected_word = None
    try:
        while detected_word is None:
            audio_data = stream.read(CHUNK, exception_on_overflow=False)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            predictions = wake_model.predict(audio_array)

            for model_name, score in predictions.items():  # type: ignore[union-attr]
                if score > WAKE_WORD_THRESHOLD:
                    detected_word = model_name
                    break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    return detected_word


def transcribe_until_over(device_index: int) -> None:
    """Transcribe speech until user says 'over'."""
    recorder = AudioToTextRecorder(
        model="small",
        language="en",
        compute_type="int8",
        input_device_index=device_index,
    )

    print("Listening... (say 'over' to stop)\n")

    try:
        while True:
            text = recorder.text()
            if text:
                text = text.strip()
                print(f">>> {text}")

                if text.lower().endswith(END_KEYWORD):
                    print("\n[Heard 'over' - returning to wake word mode]\n")
                    break
    finally:
        recorder.shutdown()


def main() -> None:
    """Main entry point."""
    load_dotenv()

    # Get device from command line or environment
    device_arg = None
    if len(sys.argv) > 1:
        device_arg = sys.argv[1]
    else:
        device_arg = os.environ.get("MUCH_MILLER_DEVICE")

    if device_arg is None:
        list_input_devices()
        print("Usage: python -m much_miller.main <device_name_or_index>")
        print("   or: MUCH_MILLER_DEVICE=Samson python -m much_miller.main")
        return

    # Resolve device index
    if device_arg.isdigit():
        device_index = int(device_arg)
    else:
        device_index = find_device_by_name(device_arg)
        if device_index is None:
            print(f"No input device matching '{device_arg}' found.")
            list_input_devices()
            return

    device_info = sd.query_devices(device_index)
    print(f"Using device: [{device_index}] {device_info['name']}\n")

    # Initialize TTS speaker
    speaker: SpeakerPort | None = None
    model_path_str = os.environ.get("MUCH_MILLER_MODEL_PATH")
    if model_path_str:
        model_path = Path(model_path_str)
        if model_path.exists():
            print(f"Loading TTS model: {model_path}")
            speaker = PiperSpeaker(model_path=model_path)
        else:
            print(f"Warning: TTS model not found at {model_path}")
    else:
        print("Warning: MUCH_MILLER_MODEL_PATH not set, TTS disabled")

    # Load wake word model
    print("Loading wake word models...")
    wake_model = WakeWordModel()
    wake_words = list(wake_model.models.keys())
    print(f"Wake words: {wake_words}\n")

    print("=" * 50)
    print("Much Miller ready!")
    print(f"Say a wake word to start: {', '.join(wake_words)}")
    print("Say 'over' to return to wake word listening")
    print("Ctrl+C to quit")
    print("=" * 50 + "\n")

    try:
        while True:
            # Phase 1: Listen for wake word
            print("Listening for wake word...")
            detected = listen_for_wake_word(device_index, wake_model)
            print(f"\n*** Wake word detected: {detected} ***\n")

            # Phase 2: Respond with TTS
            if speaker is not None:
                speaker.say("Hello Romilly")

            # Phase 3: Transcribe until "over"
            transcribe_until_over(device_index)

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
