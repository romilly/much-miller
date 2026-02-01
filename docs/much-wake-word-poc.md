# Wake-word proof of concept for Much

## Goal

Build a simple wake-word detector that:
1. Continuously captures audio from the microphone
2. Sends chunks to polwarth's transcription service
3. Triggers an action when "much" is detected in the transcription
4. Phase 2: Responds with TTS

## Architecture

```
[Microphone] → [Audio chunks] → [POST to trend/api/transcribe] → [Check for "much"] → [Action]
```

## Project structure

```
much-miller/
├── src/
│   └── wake_word/
│       ├── __init__.py
│       ├── audio.py         # Mic capture
│       ├── transcriber.py   # Client for polwarth API
│       ├── detector.py      # Wake word matching
│       ├── speaker.py       # TTS (phase 2)
│       └── main.py          # Entry point
├── pyproject.toml
└── README.md
```

## Dependencies

```toml
[project]
dependencies = [
    "sounddevice",      # Mic capture (simpler than pyaudio)
    "numpy",
    "httpx",            # Async HTTP client
    "scipy",            # WAV encoding
    "pyttsx3",          # TTS (phase 2)
]
```

## Implementation

### audio.py - Microphone capture

```python
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import io

SAMPLE_RATE = 16000
CHANNELS = 1

def record_chunk(duration_seconds: float = 2.0) -> bytes:
    """Record audio and return as WAV bytes."""
    samples = int(duration_seconds * SAMPLE_RATE)
    audio = sd.rec(samples, samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    
    # Encode as WAV
    buffer = io.BytesIO()
    wavfile.write(buffer, SAMPLE_RATE, audio)
    return buffer.getvalue()
```

### transcriber.py - Great-dictator client

```python
import httpx

# Both services run on trend - use localhost
TRANSCRIBE_URL = "http://localhost:8000/api/transcribe"
TIMEOUT = 10.0

def transcribe(audio_wav: bytes) -> str:
    """Send audio to great-dictator, return transcribed text."""
    response = httpx.post(
        TRANSCRIBE_URL,
        content=audio_wav,
        headers={"Content-Type": "audio/wav"},
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()["text"]
```

### detector.py - Wake word matching

```python
import re

WAKE_WORDS = ["much", "hey much", "hi much", "okay much"]

def contains_wake_word(text: str) -> bool:
    """Check if transcription contains wake word."""
    text_lower = text.lower()
    return any(word in text_lower for word in WAKE_WORDS)

def extract_command(text: str) -> str | None:
    """Extract command following wake word, if any."""
    text_lower = text.lower()
    for word in WAKE_WORDS:
        if word in text_lower:
            parts = text_lower.split(word, 1)
            if len(parts) > 1 and parts[1].strip():
                return parts[1].strip()
    return None
```

### main.py - Entry point (Phase 1)

```python
from wake_word.audio import record_chunk
from wake_word.transcriber import transcribe
from wake_word.detector import contains_wake_word, extract_command
import time

CHUNK_DURATION = 2.0  # seconds
OVERLAP = 0.5         # seconds of overlap between chunks

def main():
    print("Listening for wake word 'much'... (Ctrl+C to stop)")
    
    while True:
        try:
            audio = record_chunk(CHUNK_DURATION)
            text = transcribe(audio)
            
            if text.strip():
                print(f"  [{text}]")  # Show what was heard
            
            if contains_wake_word(text):
                print(f">>> WAKE WORD DETECTED!")
                command = extract_command(text)
                if command:
                    print(f">>> Command: {command}")
                    
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
```

## Phase 2: Add TTS response

### speaker.py

```python
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def say(text: str):
    """Speak text aloud."""
    engine.say(text)
    engine.runAndWait()
```

### Update main.py

```python
from wake_word.speaker import say

# In the detection block:
if contains_wake_word(text):
    print(f">>> WAKE WORD DETECTED!")
    say("Yes?")
    # Then could record again for the command...
```

## Configuration

Consider a config file or environment variables:

```python
# config.py
TRANSCRIBE_URL = os.getenv("TRANSCRIBE_URL", "http://localhost:8000/api/transcribe")
WAKE_WORDS = os.getenv("WAKE_WORDS", "much,hey much").split(",")
CHUNK_DURATION = float(os.getenv("CHUNK_DURATION", "2.0"))
```

## Running

```bash
# From the much-miller directory
cd much-miller
pip install -e .
python -m wake_word.main
```

## Future improvements

- Overlapping chunks to catch wake words split across boundaries
- Confidence threshold (if Whisper provides word-level confidence)
- "Listening" mode after wake word - longer recording for full command
- Integration with great-dictator for dictation mode
- Microphone activity detection (VAD) to avoid transcribing silence
