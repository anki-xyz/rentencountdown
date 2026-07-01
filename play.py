from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import config


def _find_player() -> str:
    for candidate in config.AUDIO_PLAYER_CANDIDATES:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(
        "Kein Audioplayer gefunden. Installiere 'alsa-utils' für 'aplay'."
    )


def play_wav(wav_file: Path) -> None:
    player = _find_player()
    cmd = [player, "-q", str(wav_file)]
    subprocess.run(cmd, check=True)
