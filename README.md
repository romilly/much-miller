# much-miller

Local AI assistant with speech interface.

*Named after Much the Miller's Son, one of Robin Hood's Merry Men - a loyal, humble companion rather than a flashy presence.*

## Status: Working Prototype

The core voice loop is now functional:
1. **Wake word detection** - openWakeWord (listens for "hey jarvis", "alexa", etc.)
2. **TTS response** - Piper says "Hello Romilly"
3. **Speech transcription** - RealtimeSTT with faster-whisper
4. **End keyword** - Say "over" to return to wake word listening

Custom wake word ("hey much") training is in progress.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run with device name (partial match)
python -m much_miller.main Samson

# Or set device in environment
export MUCH_MILLER_DEVICE=Samson
python -m much_miller.main
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `MUCH_MILLER_DEVICE` | Audio input device name or index |
| `MUCH_MILLER_MODEL_PATH` | Path to Piper TTS model (ONNX file) |

### List Audio Devices

```bash
python -m much_miller.main
# Shows available input devices if no device specified
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     much-miller (trend)                      │
├─────────────────────────────────────────────────────────────┤
│  openWakeWord          RealtimeSTT           Piper TTS      │
│  (wake word detection) (faster-whisper)      (speech out)   │
│                        CPU inference                         │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Library | Purpose |
|-----------|---------|---------|
| Wake word | openWakeWord | Lightweight, runs on CPU, multiple wake words |
| Transcription | RealtimeSTT + faster-whisper | Real-time STT with VAD |
| TTS | Piper | Fast local text-to-speech |
| Audio | sounddevice + PyAudio | Device enumeration and capture |

## Dependencies

```
openwakeword      # Wake word detection
RealtimeSTT       # Real-time speech-to-text
piper-tts         # Text-to-speech
sounddevice       # Audio device enumeration
pyaudio           # Audio capture for openWakeWord
```

## Project Structure

```
src/much_miller/
├── main.py                 # Main entry point - wake word + transcription loop
└── wake_word/
    ├── ports/              # Abstract interfaces
    │   ├── audio_recorder.py
    │   └── speaker.py
    └── adapters/           # Implementations
        ├── sounddevice_recorder.py
        ├── piper_speaker.py
        ├── fake_recorder.py
        └── fake_speaker.py
```

## Development

```bash
# Install dependencies
source venv/bin/activate
uv pip install -r requirements.txt
uv pip install -r requirements-test.txt

# Run tests
pytest

# Type check
pyright src/
```

## Roadmap

See `docs/much-rearchitecture-plan.md` for the full architecture plan.

### Completed (Phase 1)
- [x] Validate OpenAI Whisper on polwarth (GPU)
- [x] Test RealtimeSTT on trend (CPU)
- [x] Test openWakeWord
- [x] Clean up old VAD-based code
- [x] Working main.py with wake word → TTS → transcription → "over" loop

### Next Steps
- [ ] Train custom "hey much" wake word
- [ ] Build transcription-service (FastAPI on polwarth)
- [ ] Add intent routing (Claude API)
- [ ] Music/radio control integration

## Related Projects

- **the-great-dictator** - Browser-based dictation app
- **video-transcriber** - Video → markdown transcription
- **arxiv-librarian** - Research paper monitoring
- **john-dee** - Personal knowledge search

## Infrastructure

| Host | Hardware | Role |
|------|----------|------|
| **trend** | Intel Linux (no GPU) | Development, microphone, Much prototype |
| **polwarth** | Intel Linux, NVIDIA 3060 | GPU transcription (24/7 once Ollama moves to xavier) |

---

*Updated 2 February 2026*
