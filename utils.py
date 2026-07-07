from __future__ import annotations

import logging
import os
import random
from datetime import date, datetime
from pathlib import Path

import config

ENCOURAGING_PHRASES = [
    "Du schaffst das!",
    "Das sitzen wir auf einer Backe ab!",
    "Das geht ganz einfach!",
    "Jeder Tag bringt dich ein Stueck näher ans Ziel.",
    "Bald gehört der Wecker nicht mehr dir.",
    "Der Endspurt läuft, und du machst das grossartig.",
    "Noch ein bisschen durchhalten, dann beginnt die freie Zeit.",
    "Die Rente winkt schon freundlich aus der Ferne.",
    "Mit jedem Morgen wird der Abstand kleiner.",
    "Du bist auf der Zielgeraden.",
    "Bald ist mehr Zeit fuer alles, was Freude macht.",
    "Der Countdown tickt zu deinen Gunsten.",
    "Jeder Arbeitstag weniger ist ein kleiner Sieg.",
    "Das Ziel ist näher, als es sich manchmal anfuehlt.",
    "Bald kannst du den Tag in deinem eigenen Tempo starten.",
    "Die Vorfreude darf ruhig jeden Tag grösser werden.",
    "Stück fuer Stück rückt die Freiheit naeher.",
    "Der Kalender arbeitet für dich.",
    "Noch ein paar Schritte, dann ist es geschafft.",
    "Bald beginnt ein richtig schönes neues Kapitel.",
    "Eine neue Rente ist wie ein neues Leben!",
    "Der Acker ruft schon!",
    "Endlich mal Zeit um was zu arbeiten.",
    "Was ist gelb und kann nicht schwimmen? Ein Bagger! Haha!"
]


def ensure_directories() -> None:
    config.APP_DIR.mkdir(parents=True, exist_ok=True)
    config.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> logging.Logger:
    ensure_directories()

    logger = logging.getLogger("renten_countdown")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    os.environ.setdefault("PATH", config.DEFAULT_PATH)
    return logger


def days_until_retirement(today: date | None = None) -> int:
    today = today or date.today()
    return (config.RETIREMENT_DATE - today).days


def retirement_status_text(today: date | None = None) -> tuple[int, str, str]:
    today = today or date.today()
    days = days_until_retirement(today)

    if days > 1:
        short = f"Noch {days} Tage"
        spoken = (
            f"Lieber {config.PERSON_NAME}, du hast nur noch {days} Tage bis zur Rente. "
            f"{random.choice(ENCOURAGING_PHRASES)}"
        )
    elif days == 1:
        short = "Noch 1 Tag"
        spoken = (
            f"Lieber {config.PERSON_NAME}, du hast nur noch einen Tag bis zur Rente."
        )
    elif days == 0:
        short = "Heute Rente!"
        spoken = (
            f"Lieber {config.PERSON_NAME}, heute ist dein erster Tag in der Rente. "
            "Herzlichen Glückwunsch!"
        )
    elif days == -1:
        short = "Seit 1 Tag"
        spoken = (
            f"Lieber {config.PERSON_NAME}, du bist seit einem Tag in Rente. "
            "Genieß es!"
        )
    else:
        retired_days = abs(days)
        short = f"Seit {retired_days} Tagen"
        spoken = (
            f"Lieber {config.PERSON_NAME}, du bist seit {retired_days} Tagen in Rente."
        )

    date_line = config.RETIREMENT_DATE.strftime("Rente ab %d.%m.%Y")
    return days, short, spoken + " ", date_line


def now_string() -> str:
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
