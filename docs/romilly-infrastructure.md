# Romilly's Infrastructure Reference

A reference document for hardware and services across personal projects. Share this with Claude Code and other AI assistants for context.

*Last updated: 2 February 2026*

---

## Network Overview

All hosts on 192.168.1.x local network. Gateway at .254.

---

## Workstations

### trend.local (.100, .101)

| Spec | Value |
|------|-------|
| IP | 192.168.1.100 (ethernet), .101 (wifi) |
| RAM | 64 GB |
| CPU | Slow-ish (compact form factor trade-off) |
| GPU | None |
| Role | Primary development machine |
| Availability | During working hours |

**Best for**: Development, testing, CPU-bound tasks, orchestration.

**Not suitable for**: GPU-accelerated inference, heavy computation.

---

### polwarth.local (.229)

| Spec | Value |
|------|-------|
| IP | 192.168.1.229 |
| RAM | 128 GB |
| GPU | NVIDIA 3060 (12 GB VRAM) |
| Role | GPU inference, Ollama hosting |
| Availability | **6 AM - 6 PM only** for interactive GPU work |

**Constraints**:
- PSU possibly under-powered for current hardware
- Reboots are problematic - avoid if possible
- Runs Ollama cron jobs every evening (usually <1 hour, occasionally ~12 hours)
- **Do not schedule GPU work outside 6 AM - 6 PM**

**Best for**: Daytime GPU inference (Whisper, Ollama, etc.), batch processing.

**Current services**:
- Ollama (evening cron jobs for arXiv Librarian summarisation)

---

## Jetson Devices

### xavier.local (.194)

| Spec | Value |
|------|-------|
| IP | 192.168.1.194 |
| Hardware | Jetson Xavier AGX 16GB |
| RAM | 16 GB (shared CPU/GPU) |
| GPU | Volta architecture, 512 CUDA cores |
| Role | Always-on GPU inference |
| Availability | 24/7 |

**Active projects**: llm-bench

**Notes**:
- Slower than polwarth but always available
- Faster-Whisper installed (after significant effort)
- ARM architecture - some packages require special handling

**Best for**: 24/7 services requiring GPU, always-available transcription endpoint.

**Current services**:
- Faster-Whisper instance

---

## Raspberry Pi Devices

### pi5-16gb.local (.206)

| Spec | Value |
|------|-------|
| IP | 192.168.1.206 |
| Hardware | Raspberry Pi 5, 16GB RAM |
| Role | Dev/experimentation |
| Availability | 24/7 |

**Active projects**: arrow, course_platform_clean, ollama-oracle, pymex

---

### pi5-postgres.local (.84)

| Spec | Value |
|------|-------|
| IP | 192.168.1.84 |
| Hardware | Raspberry Pi 5 + 4TB NVMe |
| Role | **Production** Semantic Scholar database |
| Storage | 4 TB NVMe |
| Availability | 24/7 |

**Active projects**: s2ag-corpus, mistral-planner, pico-c, streamlit_spikes

**Notes**:
- Hosts the 220M+ paper Semantic Scholar corpus
- Initial import takes over a day

---

### pi5-corpus.local (.230)

| Spec | Value |
|------|-------|
| IP | 192.168.1.230 |
| Hardware | Raspberry Pi 5 |
| Role | **Experimental** Semantic Scholar database + data files |
| Availability | 24/7 |

**Notes**:
- Experimental copy of the database
- Stores all downloaded data files used to populate the corpus

---

### s2ag.local (.67)

| Spec | Value |
|------|-------|
| IP | 192.168.1.67 |
| Hardware | Raspberry Pi |
| Role | Production cron jobs |
| Availability | 24/7 |

**Active projects**: arxiv-librarian, github_star_tracker, hack, skno-sna

**Current services**:
- arXiv Librarian daily cron jobs

---

### watcher.local (.92)

| Spec | Value |
|------|-------|
| IP | 192.168.1.92 |
| Hardware | Raspberry Pi 4 + TV HAT |
| Role | Freeview TV reception |
| Software | TVheadend |
| Location | Hadleigh, Suffolk (Sudbury transmitter) |
| Availability | 24/7 |

**Notes**:
- Successfully receiving SD Freeview broadcasts
- Will feed recordings to transcription infrastructure
- Future: watcher-on-the-Pi for news transcription

---

### lazymk4.local

| Spec | Value |
|------|-------|
| Hardware | Raspberry Pi + LiDAR sensor |
| Role | Lazydoro - automated pomodoro timer |
| Availability | 24/7 |

**Active projects**: tdd-lazydoro

**Notes**:
- Uses LiDAR to detect when seated at desk
- Automated pomodoro timing based on presence
- Future: will feed presence data to Much for context awareness

---

### studyzero.local (.228)

| Spec | Value |
|------|-------|
| IP | 192.168.1.228 |
| Hardware | Raspberry Pi Zero |
| Role | Infrastructure documentation website |
| Availability | 24/7 |

**Active projects**: zero-web

**Notes**:
- Hosts a static website with useful infrastructure info
- Auto-generates content via Python script that uses SSH to explore what's on each Pi/Xavier
- Source of truth for "what runs where"

---

### scholar2.local (.126)

| Spec | Value |
|------|-------|
| IP | 192.168.1.126 |
| Hardware | Raspberry Pi |
| Role | Legacy - early Semantic Scholar work |
| Availability | 24/7 |

**Notes**:
- Early version of Semantic Scholar database (outdated)
- Has outdated Dyalog APL for Pi installed
- **Candidate for repurposing** |

---

## Incoming Hardware

### Jetson Orin 8GB
- **Status**: Arriving soon
- **Role**: TBD - additional always-on GPU capacity

### Jetson Xavier AGX 32GB
- **Status**: Arriving later this month
- **Role**: TBD - more capable than current 16GB xavier

### Pi 5 + AI HAT+ 2 (10GB)
- **Status**: Arriving later this month
- **Hardware**: Hailo-10H accelerator, 40 TOPS (INT4), 8GB dedicated RAM
- **Role**: Much voice assistant - local STT, intent routing, TTS
- **Notes**: New 10GB version runs GenAI models

---

## Service Allocation Guidelines

### Always-on services (24/7)
Deploy to: **xavier**, **s2ag**, **Pi devices**

Examples:
- API endpoints that must always respond
- Monitoring services
- Database hosting

### GPU-intensive daytime work
Deploy to: **polwarth** (6 AM - 6 PM only)

Examples:
- Interactive transcription with low latency requirements
- Model fine-tuning
- Batch processing that can complete within working hours

### GPU work that may run overnight
Deploy to: **xavier** (slower but always available)

Examples:
- Transcription endpoints for async processing
- Services where latency is less critical

### CPU-only work
Deploy to: **trend** or any Pi

Examples:
- Web UIs
- Orchestration services
- Lightweight APIs

---

## Network Notes

- All hosts on 192.168.1.x local network
- Gateway at 192.168.1.254 (ports 80, 443)
- Cloudflare tunnels available for external HTTPS access (free plan: 1000 tunnels, no bandwidth limits)
- Cloudflare Access for authentication (free for up to 50 users)

**Unidentified devices**:
- 192.168.1.93 - unknown
- 192.168.1.133 - unknown (90ms ping suggests wireless)

---

## Software Environment Notes

### Package Installation Challenges

**Faster-Whisper**:
- Works on xavier (ARM/Jetson) after significant effort
- **Fails on polwarth** - ctranslate2 compilation issues
- Consider OpenAI Whisper as easier alternative on x86

**OpenAI Whisper**:
- Pure PyTorch - `pip install openai-whisper`
- Should work on polwarth without issues
- ~4x slower than Faster-Whisper but much easier to install

**RealtimeSTT**:
- Untested on Jetson - may have ARM-specific audio library issues
- Can use either Faster-Whisper or OpenAI Whisper as backend

**Porcupine (wake-word)**:
- Proprietary - requires Picovoice access key
- Free tier: 3 custom wake words, usage limits

**openWakeWord**:
- Fully open source alternative to Porcupine
- No keys or limits
- Can run 15-20 models on Pi 3

---

## Quick Reference: What Runs Where

| Service/Project | Host | Notes |
|-----------------|------|-------|
| Faster-Whisper | xavier | 24/7 transcription |
| Ollama | polwarth | Evening cron jobs |
| arXiv Librarian | s2ag | Daily cron |
| s2ag-corpus (production) | pi5-postgres | Semantic Scholar DB |
| s2ag-corpus (experimental) | pi5-corpus | + data files |
| TVheadend | watcher | Freeview reception |
| Lazydoro | lazymk4 | LiDAR presence detection |
| Infrastructure dashboard | studyzero | Auto-generated via SSH |
| Development | trend | Primary workstation |

---

*This document should be updated when hardware or service allocation changes.*
