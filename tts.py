from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import config


def _find_tts_binary() -> str:
    """Return a valid Piper binary path.

    Prefers `config.PIPER_BIN` if set; falls back to locating `piper` on PATH.
    Raises FileNotFoundError if Piper cannot be found.
    """
    try:
        piper_path = config.PIPER_BIN
    except AttributeError:
        piper_path = None

    if piper_path:
        p = Path(piper_path)
        if p.exists() and p.is_file():
            return str(p)

    path = shutil.which("piper") or shutil.which("piper.exe")
    if path:
        return path

    raise FileNotFoundError("Kein Piper-Binary gefunden. Setze config.PIPER_BIN oder installiere 'piper'.")


def synthesize_to_wav(text: str, output_file: Path | None = None) -> Path:
    """Synthesize `text` to a WAV using Piper.

    - Always uses Piper and writes to `output_file` (defaults to `config.TEMP_WAV_FILE`).
    - Feeds Piper through an `echo text | piper ...` style pipeline.
    """
    output_file = output_file or config.TEMP_WAV_FILE
    output_file.parent.mkdir(parents=True, exist_ok=True)

    piper_bin = _find_tts_binary()

    cmd: list[str] = [piper_bin]
    model = getattr(config, "PIPER_MODEL", None)
    if model:
        cmd += ["--model", str(model)]

    out_flag = getattr(config, "PIPER_OUTPUT_FLAG", "--output_file")
    cmd += [out_flag, str(output_file)]

    try:
        echo = subprocess.Popen(
            ["echo", text],
            stdout=subprocess.PIPE,
        )
        subprocess.run(cmd, stdin=echo.stdout, check=True)
        if echo.stdout:
            echo.stdout.close()
        echo.wait()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Piper synthesis failed: {exc}") from exc

    return output_file
