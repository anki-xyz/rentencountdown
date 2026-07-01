from pathlib import Path
from datetime import date

# Personalisierung
PERSON_NAME = "Ludwig"

# 1. Tag in Rente
RETIREMENT_DATE = date(2028, 5, 31)

# OLED
OLED_I2C_PORT = 1
OLED_I2C_ADDRESS = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 32
OLED_ROTATE = 0

# TTS / Audio
TTS_BINARY_CANDIDATES = ("piper", "espeak-ng", "espeak")
TTS_VOICE = "de"
TTS_SPEED_WPM = 145
TTS_VOLUME = 180  # 0..200
AUDIO_PLAYER_CANDIDATES = ("aplay",)

# Piper-specific defaults (adjust to your environment if different)
PIPER_BIN = Path.home() / "piper-venv" / "bin" / "piper"
# Path to a Piper model (onnx). If None, code will try to call piper without --model.
PIPER_MODEL = Path.home() / ".local" / "share" / "piper" / "de_DE-kerstin-low.onnx"
PIPER_OUTPUT_FLAG = "--output_file"

# Dateien / Logging
APP_DIR = Path.home() / ".local" / "share" / "renten_countdown"
AUDIO_DIR = APP_DIR / "audio"
LOG_DIR = APP_DIR / "logs"
TEMP_WAV_FILE = AUDIO_DIR / "latest.wav"
LOG_FILE = LOG_DIR / "app.log"

# Kleine Sicherheitsreserve für Cron-Umgebung
DEFAULT_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
