# much-miller

Local AI assistant with speech, browser and touchscreen interfaces..

# Personal Infrastructure Projects

A family of related projects for speech-to-text, video transcription, voice interfaces, and personal knowledge management.

---

## video-transcriber

**Status**: Published on PyPI  
**Repo**: https://github.com/romilly/video-transcriber

A Python library that extracts visually distinct frames from videos and transcribes audio using Whisper. Designed for turning presentation recordings into portable markdown documentation.

### Features
- Smart slide detection using perceptual hashing (captures only distinct frames)
- Audio transcription via Whisper (runs locally)
- Timeline merging - associates transcribed audio with corresponding slides
- Portable output - zip file containing markdown and images

### Output Structure
```
my-presentation_transcript.zip
├── transcript.md
└── img/
    ├── frame_000.png
    ├── frame_001.png
    └── ...
```

### Options
- Model size: tiny, base, small, medium, large-v3
- Sample interval for slide detection
- Timestamps in output
- Audio-only mode for podcasts/interviews

---

## video-transcriber-gui

**Status**: Published on PyPI  
**Repo**: https://github.com/romilly/video-transcriber-gui

A Textual-based TUI wrapper for video-transcriber. Provides a file browser for selecting videos and a simple interface for transcription.

---

## the-great-dictator

**Status**: In development  
**Host**: polwarth (Intel Linux box with GPU)

A browser-based dictation app for family use. Users speak into their browser; audio is transcribed server-side and saved per-user.

### Architecture
- FastAPI backend with SQLite for user accounts and saved dictations
- Faster-Whisper with GPU acceleration for STT
- Cloudflare tunnel for HTTPS access from anywhere
- Cloudflare Access for authentication (free for up to 50 users)

### Key Design Decisions
- Everything runs on polwarth - no need to split across multiple machines
- Cloudflare Access provides the login wall; app reads `Cf-Access-Authenticated-User-Email` header
- Dictations scoped by authenticated email address

---

## watcher-on-the-Pi

**Status**: Planned

A Raspberry Pi-based system to watch and transcribe free-to-air television broadcasts. Completely legitimate - just receiving public broadcasts and taking notes.

### Concept
- DVB-T tuner receives Freeview broadcasts
- Audio stream piped through Whisper/Moonshine for continuous transcription
- Transcripts stored and indexed for search and summarisation
- No authentication, no APIs, no terms of service concerns

### Potential Capabilities
- "What's in the news?" - summarise recent BBC News transcripts
- Search broadcasts for specific topics
- Alert on keywords or topics of interest
- Feed transcripts into knowledge base

### Hardware Options
- USB DVB-T dongle (cheap, widely available)
- Pi 5 + AI HAT+ 2 for on-device STT
- Or route audio to polwarth for GPU-accelerated transcription

### Open Questions
- Store video recordings or just transcripts?
- Which channels to monitor (BBC News, Parliament, etc.)?
- Storage and retention policy

---

## gmail_reader

**Status**: In use  
**Repo**: https://github.com/romilly/gmail_reader

A Python library for reading Gmail messages via the Gmail API, converting HTML content to Markdown, and storing messages in PostgreSQL.

### Features
- Gmail API integration with OAuth2 authentication
- HTML to Markdown conversion with smart cleaning (removes tracking images, boilerplate)
- Email address extraction from headers
- PostgreSQL storage with markdown column
- Idempotent sync - fetches incrementally, safe to interrupt and resume
- Batch export to Markdown files
- Hexagonal architecture for testability

### Key Capabilities
```python
# Sync messages from a specific sender
result = sync_messages(
    reader=reader,
    repository=repository,
    sender='newsletter@example.com',
    after_date='2024/01/01',
    verbose=True
)
```

### Architecture
- **Ports**: `MessageReaderPort`, `MessageRepositoryPort`
- **Adapters**: `GmailMessageReader` (Gmail API), `PostgresMessageRepository` (PostgreSQL)

---

## John Dee

**Status**: In use  
**Repo**: https://github.com/romilly/john-dee

*Named after the Elizabethan polymath, mathematician, and keeper of the largest private library in England*

A FastAPI web application providing browser-based search access to personal knowledge stores, starting with Logseq.

### Features
- Web UI at `/search` for browser-based searching
- Three search modes: full-text (FTS), semantic (embeddings), hybrid
- JSON API for programmatic access
- Hexagonal architecture

### Stack
- PostgreSQL with pgvector for document storage
- Ollama with nomic-embed-text for semantic search
- logseq-searcher library for Logseq integration

### API
```
GET /search?q=query&type=hybrid  # Web search
POST /api/search                  # JSON API
GET /api/sources                  # List sources
```

---

## arXiv Librarian

**Status**: In production (runs on s2ag Pi)  
**Repo**: https://github.com/romilly/arxiv-librarian

Monitors, analyzes, and summarizes research papers from arXiv and bioRxiv, tracking research trends over time.

### Features
- Automated paper collection from arXiv and bioRxiv APIs
- AI-powered summarization using Ollama (qwen2.5:7b on polwarth's GPU)
- Trend analysis - tracks frequency of acronyms and terms over time
- Flask web interface for visualization
- PostgreSQL storage with full-text search on AI summaries
- Hexagonal architecture with comprehensive test coverage

### Production Setup
- Runs on **s2ag** (Raspberry Pi) with daily cron jobs
- Uses **polwarth** for GPU-accelerated summarization (NVIDIA 3060)
- Processes up to 12,000 papers per daily run

### bioRxiv Integration
- Abstract Retriever interface for testability
- Automatic pagination and category filtering
- VCR.py for fast test execution

---

## s2ag-corpus

**Status**: In production (runs on Pi 5)  
**Repo**: https://github.com/romilly/s2ag-corpus

Imports the Semantic Scholar Academic Graph Corpus into PostgreSQL. Handles the full dataset (220M+ papers, 2.6B+ citations) with incremental diff updates.

### Features
- Downloads and imports full S2AG dataset releases
- Applies incremental diffs from Semantic Scholar API
- Supports: abstracts, authors, citations, paper-ids, papers, publication-venues, tldrs
- Citation graph visualization (generates SVG from paper relationships)

### Hardware Requirements
- ~1TB storage for downloads
- Large database volume (4TB NVMe recommended)
- Initial import takes over a day on Pi 5

### Citation Graphs
Generates interactive SVG visualizations of citation networks - hover for paper details, click to open in Semantic Scholar.

---

## s2ag-web-researcher

**Status**: In development  
**Repo**: https://github.com/romilly/s2ag-web-researcher

Web interface for accessing and caching Semantic Scholar Academic Graph data. Uses the S2AG API with local caching.

### Features
- Access to S2AG via new API
- Local caching of results
- Can create Logseq-formatted pages for papers

---

## Much: Personal AI Assistant

**Status**: Planned (long-term)

A local voice assistant designed to be "done right" - legitimate APIs, no ToS breaches, proper integration with personal infrastructure.

The name comes from Much the Miller's Son, one of Robin Hood's Merry Men - a loyal, humble companion rather than a flashy presence.

### Core Design Principles
- Legitimate integrations only: Official Google APIs, paid services where necessary
- Local-first where practical: Speech processing and simple commands on-device
- Incremental value: Build something simple that works, then extend

### Planned Capabilities

**Voice Interface**
- Wake-word detection (note: "Much" may have false-positive issues - consider "Hey Much")
- Speech-to-text (Moonshine for low latency, Whisper for accuracy)
- Text-to-speech
- Intent routing for command classification

**Information Access**
- Personal knowledge base via John Dee (Logseq, PostgreSQL with pgvector)
- Email via gmail_reader (Gmail API, PostgreSQL storage)
- Research papers via arXiv Librarian and s2ag-corpus
- Google Calendar queries
- News from watcher-on-the-Pi transcripts
- Stock market data (legal APIs)

**Media Control**
- Personal music library
- DAB radio (BBC Radio 3, Radio 4) via uGreen or MonkeyBoard HAT

**Context Awareness**
- Lazydoro integration: presence data from lidar sensor
- VS Code plugin: time spent on each project
- Claude Code CLI: AI-assisted coding time
- Logseq: PKM integration

### Hardware Architecture

**Pi 5 + AI HAT+ 2 ($130)**
- Hailo-10H accelerator: 40 TOPS (INT4)
- 8GB dedicated onboard RAM
- Runs Whisper/Moonshine for local STT
- Runs small LLMs for intent routing
- Keeps simple interactions local (low latency, no API cost)

**DAB Radio HAT**
- uGreen DAB Board
- Receives BBC broadcasts over the air
- Avoids BBC Sounds authentication requirements

**Pi TV Hat**
- Installed and working, will allow transcription of News and other channels.

**Pico-based Touchscreen**
- Dedicated display interface
- Lightweight, always on

### Tiered Processing
1. **Local (HAT+ 2)**: Wake-word, STT, intent classification, simple commands, TTS
2. **Claude API**: Complex queries, knowledge base reasoning

### First Milestone
Voice control of music library and Radio 3/4 - contained scope, immediate daily value, exercises the core pipeline.

## Running the Wake Word Detector

Requires the transcriber service running on localhost:8765.

```bash
source venv/bin/activate
python -m much_miller.main
```

Press Ctrl+C to stop.

---


## Related Tools

- **Faster-Whisper**: GPU-accelerated Whisper, best accuracy, runs on polwarth
- **Cloudflare Tunnels**: Free HTTPS access to home services, 1000 tunnels allowed on free plan
- **Ollama**: Local LLM hosting, used with nomic-embed-text for semantic search in John Dee
- **pgvector**: PostgreSQL extension for vector similarity search

---

## Infrastructure

| Host | Hardware | Role |
|------|----------|------|
| **polwarth** | Intel Linux, NVIDIA 3060 GPU | the-great-dictator, Faster-Whisper STT, Ollama for summarization |
| **s2ag** | Raspberry Pi | arXiv Librarian cron jobs, production database |
| **Pi 5** | Raspberry Pi 5 + 4TB NVMe | s2ag-corpus (Semantic Scholar database) |
| **Pi 4** | Pi 4 + TV Hat | Freeview TV |
| **Future** | Pi 5 + AI HAT+ 2 | Much voice assistant, local STT/intent routing |

---

*Updated 31 January 2026*
