from __future__ import annotations

import argparse

from oled import write_countdown
from play import play_wav
from tts import synthesize_to_wav
from utils import setup_logging


def test_oled() -> None:
    write_countdown(
        headline="Testanzeige",
        date_line="OLED funktioniert",
        footer="Hallo Ludwig",
    )


def test_tts_audio() -> None:
    wav_file = synthesize_to_wav(
        "Lieber Ludwig, dies ist ein Test der Sprachansage."
    )
    play_wav(wav_file)


def main() -> None:
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Hardware-Test für Renten-Countdown")
    parser.add_argument(
        "--only",
        choices=("oled", "audio", "all"),
        default="all",
        help="Nur einen Teil testen",
    )
    args = parser.parse_args()

    logger.info("Test gestartet: %s", args.only)

    if args.only in ("oled", "all"):
        test_oled()

    if args.only in ("audio", "all"):
        test_tts_audio()

    logger.info("Test beendet: %s", args.only)


if __name__ == "__main__":
    main()
