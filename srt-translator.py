#!/usr/bin/env python3
import os
import re
import sys
from typing import List, Tuple, Optional

import requests

try:
    from googletrans import Translator as GoogleTranslator
except ImportError:
    GoogleTranslator = None


def parse_srt(path: str) -> List[Tuple[str, str, List[str]]]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks_raw = re.split(r"\n\s*\n", content.strip(), flags=re.MULTILINE)
    blocks = []

    for block in blocks_raw:
        lines = block.splitlines()
        if len(lines) < 2:
            continue
        index_line = lines[0].strip()
        timestamp_line = lines[1].strip()
        text_lines = [l.rstrip("\n") for l in lines[2:]]
        blocks.append((index_line, timestamp_line, text_lines))

    return blocks


def write_srt(path: str, blocks: List[Tuple[str, str, List[str]]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i, (index_line, timestamp_line, text_lines) in enumerate(blocks):
            f.write(str(index_line) + "\n")
            f.write(timestamp_line + "\n")
            for line in text_lines:
                f.write(line + "\n")
            if i != len(blocks) - 1:
                f.write("\n")


def translate_libretranslate(
    text: str,
    source_lang: str,
    target_lang: str,
    url: str = "https://libretranslate.com",
    api_key: Optional[str] = None,
) -> str:
    endpoint = url.rstrip("/") + "/translate"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text",
    }
    if api_key:
        payload["api_key"] = api_key

    resp = requests.post(endpoint, json=payload, timeout=30)

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"LibreTranslate error {resp.status_code}: {resp.text}"
        ) from e

    out = resp.json()

    if isinstance(out, dict) and "translatedText" in out:
        return out["translatedText"]
    if isinstance(out, list) and out and "translatedText" in out[0]:
        return out[0]["translatedText"]

    raise RuntimeError(f"Unexpected LibreTranslate response: {out}")


def translate_deepl(
    text: str,
    target_lang: str,
    api_key: str,
    free: bool = True,
) -> str:
    base_url = "https://api-free.deepl.com/v2/translate" if free else "https://api.deepl.com/v2/translate"
    headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
    data = {"text": text, "target_lang": target_lang.upper()}
    resp = requests.post(base_url, data=data, headers=headers, timeout=30)
    resp.raise_for_status()
    out = resp.json()
    try:
        return out["translations"][0]["text"]
    except Exception:
        raise RuntimeError(f"Unexpected DeepL response: {out}")


def translate_googletrans(
    text: str,
    source_lang: str,
    tar
