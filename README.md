# LM Studio — Alfred Workflow

[![Alfred Workflow](https://img.shields.io/badge/Alfred-Workflow-5C1F87?logo=alfred)](https://www.alfredapp.com/)
[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LM Studio](https://img.shields.io/badge/LM%20Studio-compatible-blueviolet)](https://lmstudio.ai/)

## Overview

An [Alfred](https://www.alfredapp.com/) workflow for controlling [LM Studio](https://lmstudio.ai/) directly from your keyboard — no clicking required.

Trigger the `lms` keyword to check server status, start or stop the local inference server (with optional CORS and LAN bindings), browse and load downloaded models with one keystroke, and unload running models individually or all at once. macOS notifications confirm each action.

<video src="assets/lms.mp4" autoplay loop muted playsinline></video>

## Usage

**Keyword:** `lms`

| Input | Action |
|-------|--------|
| `lms` | Main menu — server status, start/stop, load/unload shortcuts |
| `lms load [text]` | Browse downloaded models (filters by name); press Enter to load |
| `lms unload [text]` | Browse loaded models; press Enter to unload |

### Modifier Keys

**Start Server:**

| Modifier | Effect |
|----------|--------|
| (none) | Start server with defaults |
| `⌘` | Start with CORS enabled |
| `⌥` | Start bound to `0.0.0.0` (LAN access) |
| `⌃` | Start with CORS + LAN |

**Load Model:**

| Modifier | Effect |
|----------|--------|
| (none) | Load model with default settings |
| `⌘` | Load with maximum GPU offload |

## Requirements

- [Alfred](https://www.alfredapp.com/) with Powerpack
- [LM Studio](https://lmstudio.ai/) installed with the `lms` CLI available at `~/.lmstudio/bin/lms`
- Python 3 (ships with macOS)

## Installation

1. Download [`release/lms_alfred.alfredworkflow`](https://github.com/RomanVolkov/lms_alfred_workflow/raw/main/release/lms_alfred.alfredworkflow)
2. Double-click the file — Alfred will import it automatically
3. Confirm `lms` is the trigger keyword (configurable in Alfred Preferences → Workflows)

## Repository Structure

```
lms_alfred/
├── src/
│   ├── filter.py           # Script Filter: builds Alfred result lists
│   └── action.py           # Run Script: executes the selected action
├── scripts/
│   └── build.sh            # Packages the workflow into release/
├── assets/                 # Screenshots and demo video
├── release/
│   └── lms_alfred.alfredworkflow  # Packaged workflow (importable)
├── info.plist              # Alfred workflow definition
└── icon.png                # Workflow icon
```

## Acknowledgements

- [LM Studio](https://lmstudio.ai/) — local LLM inference engine and `lms` CLI
- [Alfred](https://www.alfredapp.com/) — macOS productivity launcher

## Author

**Roman Volkov** — [github.com/romanvolkov](https://github.com/romanvolkov)
