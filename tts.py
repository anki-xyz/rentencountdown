from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import config


def _find_tts_binary() -> str:
    # If a Piper binary path is configured and exists, prefer it.
    try:
        piper_path = config.PIPER_BIN
    except AttributeError:
        piper_path = None

    if piper_path:
        p = Path(piper_path)
        if p.exists() and p.is_file():
            return str(p)

    for candidate in config.TTS_BINARY_CANDIDATES:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(
        "Kein TTS-Binary gefunden. Installiere 'piper', 'espeak-ng' oder 'espeak'."
    )


def synthesize_to_wav(text: str, output_file: Path | None = None) -> Path:
    output_file = output_file or config.TEMP_WAV_FILE
    output_file.parent.mkdir(parents=True, exist_ok=True)

    tts_bin = _find_tts_binary()
    def _build_command_and_input(bin_path: str) -> tuple[list[str], bytes | None]:
        name = Path(bin_path).name.lower()
        # Piper: prefer passing text on stdin and specify model + output file
        if "piper" in name:
            cmd: list[str] = [bin_path]
            # add model if configured
            try:
                model = config.PIPER_MODEL
            except AttributeError:
                model = None
            if model:
                cmd += ["--model", str(model)]
            # voice may be mapped to Piper --voice if supported
            if getattr(config, "TTS_VOICE", None):
                cmd += ["--voice", config.TTS_VOICE]
            # output flag
            out_flag = getattr(config, "PIPER_OUTPUT_FLAG", "--output_file")
            cmd += [out_flag, str(output_file)]
            # Piper reads text from stdin
            return cmd, text.encode()

        # Fallback to espeak/espeak-ng style args
        if "espeak" in name:
            return (
                [
                    bin_path,
                    "-v",
                    config.TTS_VOICE,
                    "-s",
                    str(config.TTS_SPEED_WPM),
                    "-a",
                    str(config.TTS_VOLUME),
                    "-w",
                    str(output_file),
                    text,
                ],
                None,
            )

        # Generic fallback — pass output file then text as arg
        return [bin_path, str(output_file), text], None

    cmd, stdin_data = _build_command_and_input(tts_bin)
    if stdin_data is not None:
        subprocess.run(cmd, input=stdin_data, check=True)
    else:
        subprocess.run(cmd, check=True)
    return output_file
