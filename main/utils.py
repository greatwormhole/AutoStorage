from typing import Any
from barcode.writer import (
    ImageWriter,
    mm2px,
    pt2mm,
    )
from PIL import Image, ImageDraw, ImageFont
from transliterate import translit, slugify

SYSTEM_CODE = {
    '0': {'message': 'Подключение с компьютера!', 'action': 'change screen', 'scanner':'none'},
    '10': {'message': 'Отсканируйте код сотрудника!', 'action': 'Show message, scanner response2server', 'scanner': 'button'},
    '11': {'message': '-', 'action': 'connect to ws by THD', 'scanner': '-'},
    '100': {'message': '-', 'action': 'disconnect to ws by THD', 'scanner': '-'},
    '101': {'message': '-', 'action': 'ws resend message', 'scanner': '-'},
    '111': {'message': '-', 'action':'thd2client id response', 'scanner':'button'},
    '1000': {'message': 'Авторизация прошла успешно!', 'action': 'show message'},
    '1001': {'message': 'Ошибка авторизации, попробуйте снова!'},
    '1010':{'message': '-'}
}

class CustomWriter(ImageWriter):

    def __init__(self, upper_text: str, *args, **kwargs):
        self.upper_text = upper_text
        self.y_img_scale = 1.5
        self.x_img_scale = 1
        self.y_bar_scale = 10
        self.x_bar_scale = 1
        super().__init__(*args, **kwargs)

    def _init(self, code):
        width, height = self.calculate_size(len(code[0]), len(code))
        size = (int(self.x_img_scale * mm2px(width, self.dpi)), int(self.y_img_scale * mm2px(height, self.dpi)))
        self._image = Image.new(self.mode, size, self.background)
        self._draw = ImageDraw.Draw(self._image)

    def _paint_module(self, xpos, ypos, width, color):
        size = [
            (mm2px(self.x_bar_scale * xpos, self.dpi), mm2px(self.y_bar_scale * ypos, self.dpi)),
            (
                mm2px(self.x_bar_scale * xpos + width, self.dpi),
                mm2px(self.y_bar_scale * ypos + self.module_height, self.dpi),
            ),
        ]
        self._draw.rectangle(size, outline=color, fill=color)

    def _paint_text(self, xpos, ypos):

        font_size = int(mm2px(pt2mm(self.font_size), self.dpi))
        font = ImageFont.truetype(self.font_path, font_size)
        
        for subtext in self.text.split("\n"):
            width, height = font.getsize(subtext)
            pos = (
                mm2px(xpos, self.dpi) - width // 2,
                mm2px(ypos, self.dpi) + 2 * height,
            )
            self._draw.text(pos, subtext, font=font, fill=self.foreground)
            ypos += pt2mm(self.font_size) / 2 + self.text_line_distance

        for subtext in self.upper_text.split("\n"):
            width, height = font.getsize(subtext)
            pos = (
                mm2px(xpos, self.dpi) - width // 2,
                mm2px(ypos, self.dpi) - 6 * height,
            )
            self._draw.text(pos, subtext, font=font, fill=self.foreground)
            ypos += pt2mm(self.font_size) / 2 + self.text_line_distance