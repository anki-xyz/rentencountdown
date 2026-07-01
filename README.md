# Renten-Countdown für Ludwig

Dieses kleine Projekt zeigt den aktuellen Countdown auf einem SSD1306-OLED an
und spricht den Status per TTS aus.

## Projektdateien

- `main.py` – Hauptprogramm für Cron (07:00 und 19:00)
- `oled.py` – Anzeige auf dem I2C-OLED
- `tts.py` – lokale TTS-Erzeugung mit `espeak-ng`
- `play.py` – Audio-Wiedergabe über ALSA / `aplay`
- `test.py` – Hardware-Test für OLED + TTS + Audio
- `config.py` – zentrale Konfiguration
- `utils.py` – Datum, Texte, Logging

## Verdrahtung

### OLED (I2C)
- VCC -> 3V3 (Pin 1)
- GND -> GND (Pin 6)
- SDA -> GPIO 2 / SDA1 (Pin 3)
- SCL -> GPIO 3 / SCL1 (Pin 5)

### MAX98357A
- VIN -> 5V (Pin 2 oder 4)
- GND -> GND (z. B. Pin 9)
- BCLK -> GPIO 18 (Pin 12)
- LRC / LRCLK / WS -> GPIO 19 (Pin 35)
- DIN -> GPIO 21 (Pin 40)

### Lautsprecher
- an SPK+ und SPK- des MAX98357A

## System vorbereiten

```bash
sudo raspi-config
```
Dann:
- `Interface Options` -> `I2C` -> aktivieren

Danach Pakete installieren:

```bash
sudo apt update
sudo apt install -y python3-pip python3-pil python3-smbus i2c-tools alsa-utils espeak-ng
python3 -m pip install --break-system-packages -r requirements.txt
```

## I2S / Audio aktivieren

In `/boot/config.txt` diese Zeile ergänzen:

```ini
dtoverlay=hifiberry-dac
```

Danach neu starten:

```bash
sudo reboot
```

Testen:
```bash
aplay -l
```

## OLED-Adresse prüfen

```bash
i2cdetect -y 1
```

Erwartet ist oft `0x3C`. Falls dein Display stattdessen `0x3D` hat, ändere
den Wert `OLED_I2C_ADDRESS` in `config.py`.

## Testen

Nur OLED:
```bash
python3 test.py --only oled
```

Nur Audio:
```bash
python3 test.py --only audio
```

Alles:
```bash
python3 test.py
```

## Cronjob

Crontab öffnen:
```bash
crontab -e
```

Eintragen:
```cron
0 7,19 * * * cd /home/pi/renten_countdown && /usr/bin/python3 main.py >> /home/pi/.local/share/renten_countdown/logs/cron.log 2>&1
```

## Hinweis

Das OLED behält die letzte Anzeige, bis ein neues Bild geschrieben wird.
