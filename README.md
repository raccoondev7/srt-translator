
# SRT Translator
Simple Python script that translates `.srt` subtitle files while keeping all timestamps.

Example use:  
Translate movie subtitles from one language to another in-place.

## Features
- Lists all `.srt` files in the current directory
- Simple terminal menu (pick file, pick API, pick language)
- Supports three backends:
  - LibreTranslate (free HTTP API)
  - googletrans (unofficial Google Translate)
  - DeepL (requires API key)
- Auto-detects source language (where supported)
- Output file is named automatically, e.g.:
  - `movie.srt` → `movie-en.srt`
- Keeps all original timestamps and indices

## Requirements
- Python 3.7+
- Internet connection
- Python packages:
  - `requests`
  - `googletrans==4.0.0-rc1`
- (Optional) DeepL API key
- (Optional) LibreTranslate API key (if your server needs it)

## Installation
```bash
pip install -r requirements.txt
````

`requirements.txt`:

```txt
requests
googletrans==4.0.0-rc1
```

## Usage

Run in a folder with your `.srt` files:

```bash
python srt-translator.py
```

Then:

1. Choose the `.srt` file
2. Choose backend (LibreTranslate / googletrans / DeepL)
3. Enter target language code (e.g. `en`, `de`, `fr`)

The translated file will appear in the same folder, e.g. `movie-en.srt`.

## Optional: Build .exe

```bash
pip install pyinstaller
pyinstaller --onefile srt-translator.py
```

The executable will be in `dist/`.
Put your `.srt` files next to it and run.


