# 🎵 Orpheus — Music Metadata Updater

A Python tool that automatically updates metadata, lyrics, and cover art for local music files (FLAC, MP3, and more) using multiple free APIs. Includes a modern graphical interface with real-time song processing cards.

## ✨ Features

### 🔍 Smart Metadata Search
| Source | Data | Free |
|--------|------|------|
| **MusicBrainz** | Title, artist, genre, year, track | ✅ |
| **iTunes API** | Metadata + high-quality cover art | ✅ |
| **Cover Art Archive** | Official album covers | ✅ |

### 📝 Lyrics
| Source | Notes |
|--------|-------|
| **LRCLIB** | Synced + plain lyrics |
| **lyrics.ovh** | Fallback |
| **ChartLyrics** | Second fallback |

### 🎨 Modern GUI (PyQt5)
- Professional dark theme
- **Real-time song cards** showing everything that changed per file
- Processing controls: ⏸️ Pause / ▶️ Resume / ⏹️ Stop
- Report dialog at the end — choose whether to save the Excel file

### 💻 Console Mode
- Interactive menu with path validation and smart suggestions
- Emoji-rich progress log
- Detailed change summary at the end
- Optional Excel report prompt

---

## 🚀 Installation

```bash
pip install mutagen openpyxl pillow PyQt5
```

Python 3.8+ required.

---

## 📖 Usage

### GUI (recommended)
```bash
python main.py --gui
```
1. Click **Browse** to pick your music folder
2. Click **🚀 Start Update** — cards update in real time
3. Use ⏸️/⏹️ to pause or stop at any time
4. At the end, choose whether to generate an Excel report

### Console menu
```bash
python main.py
```
```
════════════════════════════════════════════════════
  🎵 Music Metadata Updater
════════════════════════════════════════════════════
  Folder : (not set)
  Mode   : Live (files will be modified)

  [1] Set music folder
  [2] Start processing
  [3] Exit
════════════════════════════════════════════════════
```
After processing you will see a full summary and be asked whether to save the report.

---

## 🎴 Song Processing Cards

Each song gets a card updated live during processing:

```
┌──────────────────────────────────────────────────────┐
│ 🎵 Crystal Castles - 1991.flac      [ ✅ Completed ] │
│ 👤 Crystal Castles  ·  🎵  1991                      │
│ 💿 Crystal Castles       🏷️ 24-bit/96kHz  📁 45.2 MB │
├──────────────────────────────────────────────────────┤
│ 📅 Year: 2008   🎸 Genre: Electronic   🖼️ Cover art  │
│ 📝 Lyrics added                                      │
└──────────────────────────────────────────────────────┘
```

### Status badges
| Badge | Meaning |
|-------|---------|
| 🔄 Processing | Currently being updated |
| ✅ Completed | Update successful |
| ➖ No changes | File was already up to date |
| ❌ Error | Something went wrong |

### Change indicators
| Emoji | Field |
|-------|-------|
| 📅 | Year / release date |
| 🎸 | Genre |
| 💿 | Album |
| 🔢 | Track number |
| 🖼️ | Cover art |
| 📝 | Lyrics |

---

## ⚙️ Configuration (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `MUSIC_DIR` | `""` | Default folder (blank = ask in GUI/menu) |
| `EXTENSIONS` | `.flac .mp3 …` | Supported formats |
| `DRY_RUN` | `False` | Simulate without writing files |
| `SLEEP_BETWEEN_REQUESTS` | `0.5` | Delay between API calls (seconds) |
| `OVERWRITE_*` | `True` | Overwrite existing genre/date/lyrics/cover/album/track |

---

## 📊 Excel Report

Generated on demand at the end of each run. Columns:

| File | Artist | Title | Album | Changes | Errors | Quality |

---

## 📁 Project Structure

```
Metadata Music/
├── main.py        # Processing logic + console menu
├── config.py      # Configuration
├── utils.py       # HTTP helpers
├── metadata.py    # MusicBrainz & iTunes search
├── lyrics.py      # Lyrics search (3 sources)
├── gui.py         # PyQt5 GUI with song cards
└── __init__.py
```

---

## 🔧 Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Not found on MusicBrainz" | Rename file to `Artist - Title.flac` format |
| No cover art | Check if the release exists in Cover Art Archive |
| No lyrics | Try renaming for a cleaner artist/title match |
| GUI won't start | `pip install PyQt5`; falls back to Tkinter automatically |

---

*Enjoy a perfectly organised music library!* 🎶
