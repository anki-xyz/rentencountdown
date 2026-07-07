from __future__ import annotations

from typing import Iterable

from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

import config


class PersistentSSD1306(ssd1306):
    def cleanup(self) -> None:
        pass


class OledDisplay:
    def __init__(self) -> None:
        serial = i2c(port=config.OLED_I2C_PORT, address=config.OLED_I2C_ADDRESS)
        self.device = PersistentSSD1306(
            serial,
            width=config.OLED_WIDTH,
            height=config.OLED_HEIGHT,
            rotate=config.OLED_ROTATE,
            persist=True,
        )
        self.font = ImageFont.load_default()

    def clear(self) -> None:
        self.device.clear()

    def write_lines(self, lines: Iterable[str]) -> None:
        lines = list(lines)[:3]

        image = Image.new("1", (self.device.width, self.device.height), color=0)
        draw = ImageDraw.Draw(image)

        y_positions = [0, 11, 22]
        for line, y in zip(lines, y_positions):
            draw.text((0, y), line[:21], font=self.font, fill=255)

        self.device.display(image)
        self.device.show()

    def show_countdown(self, headline: str, date_line: str, footer: str = "") -> None:
        lines = [headline, date_line]
        if footer:
            lines.append(footer)
        self.write_lines(lines)


def write_countdown(headline: str, date_line: str, footer: str = "") -> None:
    display = OledDisplay()
    display.show_countdown(headline, date_line, footer)
