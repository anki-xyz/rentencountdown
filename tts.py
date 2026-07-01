from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import config


def _find_tts_binary() -> str:
    for candidate in config.TTS_BINARY_CANDIDATES:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(
        "Kein TTS-Binary gefunden. Installiere 'espeak-ng' oder 'espeak'."
    )


def synthesize_to_wav(text: str, output_file: Path | None = None) -> Path:
    output_file = output_file or config.TEMP_WAV_FILE
    output_file.parent.mkdir(parents=True, exist_ok=True)

    tts_bin = _find_tts_binary()

    cmd = [
        tts_bin,
        "-v",
        config.TTS_VOICE,
        "-s",
        str(config.TTS_SPEED_WPM),
        "-a",
        str(config.TTS_VOLUME),
        "-w",
        str(output_file),
        text,
    ]
    subprocess.run(cmd, check=True)
    return output_file
