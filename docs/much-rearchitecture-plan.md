# Much Ecosystem Re-architecture Plan

## Current State

- **great-dictator**: Monolithic app doing dictation + transcription
- **transcriber**: Batch voice memo processor (Easy Voice Recorder → Whisper → Logseq)
- **xavier** (Jetson Xavier AGX 16GB): 24/7 availability, will use OpenAI Whisper (not Faster-Whisper, to simplify installation)
- **polwarth** (128GB RAM, 3060 GPU 12GB VRAM): **GPU available 6 AM - 6 PM only** (evening Ollama cron jobs)
- **trend** (64GB RAM): CPU-only workstation, primary dev machine

### Incoming Hardware (not in scope for this plan)
- Jetson Orin 8GB (soon)
- Jetson Xavier AGX 32GB (this month)
- Pi 5 + AI HAT+ 2 10GB (timing uncertain)

## Target Architecture

### Three Separate Services

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENTS                                    │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│   great-dictator    │   Much Assistant    │   Future: watcher-on-Pi │
│   (web browser)     │   (voice interface) │   (TV transcription)    │
└─────────┬───────────┴──────────┬──────────┴────────────┬────────────┘
          │                      │                       │
          ▼                      ▼                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TRANSCRIPTION SERVICES                           │
├─────────────────────────────────┬───────────────────────────────────┤
│   transcription-service         │   realtime-transcriber            │
│   (OpenAI Whisper)              │   (RealtimeSTT + openWakeWord)    │
│   Host: xavier (24/7)           │   Backend: OpenAI Whisper         │
│         or polwarth (6AM-6PM)   │   Host: xavier (24/7)             │
│   Use case: accuracy, batch     │   Use case: low latency, wake-word│
└─────────────────────────────────┴───────────────────────────────────┘
```

**Note**: All services use OpenAI Whisper (not Faster-Whisper) for simpler installation. polwarth's GPU is only available 6 AM - 6 PM due to evening Ollama cron jobs.

### Project Split

| Old | New | Purpose |
|-----|-----|---------|
| great-dictator | **great-dictator** (refactored) | Web UI, user sessions, saved dictations, calls transcription API |
| great-dictator | **transcription-service** | Stateless `/api/transcribe` endpoint (OpenAI Whisper) |
| (new) | **realtime-transcriber** | RealtimeSTT + openWakeWord for streaming/wake-word use cases |
| transcriber | (unchanged) | Batch voice memo processor → Logseq (separate workflow) |

---

## Phase 1: Validate Technology Choices

### 1.1 Install OpenAI Whisper on polwarth

```bash
pip install openai-whisper
```

Test with a simple script to confirm GPU acceleration works.

**Success criteria**: Transcribe a 30-second WAV file in under 10 seconds using `medium` model.

**Note**: polwarth GPU available 6 AM - 6 PM only.

### 1.2 Install OpenAI Whisper and RealtimeSTT on xavier

```bash
pip install openai-whisper
pip install RealtimeSTT
```

Test basic functionality - may need to configure audio input. Configure RealtimeSTT to use OpenAI Whisper as backend.

**Success criteria**: Speak into microphone, see transcription output.

### 1.3 Install RealtimeSTT on polwarth

Same as above, but using OpenAI Whisper as backend. Compare performance between xavier and polwarth.

**Success criteria**: Determine which host is better suited for real-time work (considering polwarth's time constraints).

### 1.4 Test openWakeWord

```bash
pip install openwakeword
```

Fully open source, no API keys required. Can run 15-20 models simultaneously on a Pi 3.

Test with built-in wake words first. Custom wake words can be trained if needed.

**Success criteria**: Reliable wake-word detection with low false-positive rate.

**Note**: openWakeWord is preferred over Porcupine because:
- Fully open source (no API keys, no usage limits)
- Can run multiple models simultaneously
- Lightweight enough for Pi hardware

---

## Phase 2: Build transcription-service

A minimal FastAPI service exposing Whisper (OpenAI or Faster) via HTTP. This becomes the shared transcription backend for multiple clients.

### 2.1 Project structure

```
transcription-service/
├── src/
│   └── transcription_service/
│       ├── __init__.py
│       ├── app.py           # FastAPI app
│       ├── transcriber.py   # Whisper wrapper with threading lock
│       └── config.py        # Model size, device, backend selection
├── tests/
├── pyproject.toml
└── README.md
```

### 2.2 API endpoint

```
POST /api/transcribe
Content-Type: audio/wav
Body: raw audio bytes (16kHz mono preferred, but Whisper handles resampling)

Response:
{
  "text": "transcribed text",
  "language": "en",
  "duration_seconds": 3.2
}
```

### 2.3 Key implementation details

- Threading lock to serialise access to single Whisper model instance
- Load model once at startup, reuse for all requests
- No authentication initially (internal network only)
- Health check endpoint at `/health`

### 2.4 Deployment

- Run on polwarth (or xavier as fallback)
- Systemd service for auto-restart
- No Cloudflare tunnel needed (internal service)

---

## Phase 3: Refactor great-dictator

Strip transcription logic out of great-dictator, keep the web UI and session management.

### 3.1 Changes required

- Remove Whisper/Faster-Whisper dependencies
- Add HTTP client to call transcription-service
- Keep: user authentication (Cloudflare Access), saved dictations, web UI
- Configuration: transcription service URL

### 3.2 Deployment

- Can run on any host (no GPU needed)
- Cloudflare tunnel for external HTTPS access
- Cloudflare Access for authentication

---

## Phase 4: Build realtime-transcriber Service

For Much wake-word detection and future streaming use cases.

### 4.1 Architecture decision

**Option A**: WebSocket server using RealtimeSTT
- Client streams audio over WebSocket
- Server returns transcriptions as they're ready
- Good for web-based interfaces

**Option B**: Local service with audio capture
- Runs on the device with the microphone
- Exposes results via HTTP/WebSocket
- Good for dedicated voice assistant hardware

**Recommendation**: Start with Option A on xavier for initial testing and web-based Much prototype.

### 4.2 Components

```
realtime-transcriber/
├── src/
│   └── realtime_transcriber/
│       ├── __init__.py
│       ├── wake_word.py      # openWakeWord integration
│       ├── transcriber.py    # RealtimeSTT wrapper (OpenAI Whisper backend)
│       ├── audio_capture.py  # Microphone handling
│       └── server.py         # API for results/status
├── tests/
├── pyproject.toml
└── README.md
```

### 4.3 Wake-word flow

```
[Microphone] → [openWakeWord] → wake word detected → [RealtimeSTT] → transcription
                  ↓                                      ↓
            (always listening,                    (activated only
             very low CPU)                        after wake word)
```

### 4.4 openWakeWord advantages

- No API keys or licensing concerns
- Can test multiple wake words simultaneously ("much", "hey much", "miller")
- Custom wake word training available if built-ins aren't suitable
- Runs on Pi hardware

---

## Phase 5: Integration with Much

Once realtime-transcriber is working on xavier:

1. Test wake-word detection reliability
2. Connect to intent routing (Claude API initially)
3. Add TTS for responses
4. Build web-based Much interface for testing

---

## Implementation Order

| Step | Task | Host | Dependencies |
|------|------|------|--------------|
| 1.1 | Install/test OpenAI Whisper | polwarth | None |
| 1.2 | Install/test OpenAI Whisper + RealtimeSTT | xavier | None |
| 1.3 | Install/test RealtimeSTT | polwarth | Step 1.1 |
| 1.4 | Test openWakeWord | xavier or polwarth | None |
| 2.x | Build transcription-service | xavier (24/7) | Step 1.2 |
| 3.x | Refactor great-dictator | trend or any | Step 2.x |
| 4.x | Build realtime-transcriber | xavier | Steps 1.2, 1.4 |
| 5.x | Much integration | xavier | Step 4.x |

---

## Open Questions

1. **transcription-service host**: xavier gives 24/7 availability. polwarth is faster but limited to 6 AM - 6 PM. Run on both with load balancing, or pick one?

2. **great-dictator location**: Does it need GPU? If not, can run on trend or any Pi.

3. **Wake word choice**: Test "much", "hey much", "miller" with openWakeWord. Which has lowest false-positive rate?

4. **Existing transcriber integration**: The batch voice memo processor (transcriber repo) is a separate workflow. Does it also need to use transcription-service, or keep its current embedded Whisper?

---

## Risks

- **RealtimeSTT on Jetson**: May have ARM-specific issues with audio libraries
- **openWakeWord on Jetson**: Should work (Python-based), but needs verification
- **Network latency**: great-dictator calling transcription-service over network adds ~10-50ms per request
- **OpenAI Whisper on Jetson**: Should work via PyTorch, but may be slow - needs testing
- **polwarth availability**: 6 AM - 6 PM constraint limits its usefulness for always-on services

---

*Plan created 2 February 2026 - target completion within 1 week*
