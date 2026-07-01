from __future__ import annotations

from oled import write_countdown
from play import play_wav
from tts import synthesize_to_wav
from utils import now_string, retirement_status_text, setup_logging


def main() -> None:
    logger = setup_logging()

    days, headline, spoken_text, date_line = retirement_status_text()
    footer = now_string()[11:16]

    logger.info("Starte Lauf. Resttage=%s", days)
    write_countdown(headline=headline, date_line=date_line, footer=footer)

    wav_file = synthesize_to_wav(spoken_text)
    play_wav(wav_file)

    logger.info("Lauf erfolgreich beendet.")


if __name__ == "__main__":
    main()
