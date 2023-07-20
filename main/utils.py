from typing import Any
from barcode.writer import (
    ImageWriter,
    mm2px,
    pt2mm,
    )
from barcode import Code39
from transliterate import translit
from PIL import Image, ImageDraw, ImageFont
import textwrap
from Apro.settings import MEDIA_ROOT
import os

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

MM_PER_PX = .2645833333
SYMBOL_WIDTH = 4.939
MAX_WIDTH = 35

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
        print(size)
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

        font_size = 25
        font = ImageFont.truetype(self.font_path, font_size)
        lines = textwrap.wrap(self.text, width=MAX_WIDTH)
        
        ypos += 3.8

        for line in lines:
            print(font.getsize(line))
            width, height = font.getsize(line)
            pos = (
                mm2px(xpos, self.dpi) - width // 2,
                mm2px(ypos, self.dpi) + 2 * height,
            )
            self._draw.text(pos, line, font=font, fill=self.foreground)
            ypos += pt2mm(self.font_size) / 2 + self.text_line_distance

        font_size = 12
        font = ImageFont.truetype(self.font_path, font_size)
        lines = textwrap.wrap(self.upper_text, width=MAX_WIDTH)
        
        ypos -= len(lines) * 1.5

        for line in lines:
            width, height = font.getsize(line)
            pos = (
                mm2px(xpos, self.dpi) - width // 2,
                mm2px(ypos, self.dpi) - 6 * height,
            )
            self._draw.text(pos, line, font=font, fill=self.foreground)
            ypos += 1.5

def resize_image(relative_path, width, height):
    height_px = int(height/MM_PER_PX)
    width_px = int(width/MM_PER_PX)
    path = os.path.join(MEDIA_ROOT, relative_path)
    image = Image.open(path)
    image = image.resize((width_px, height_px), Image.ANTIALIAS)
    image.save(path)

def generate_barcode(id, title):

    article = translit(id, language_code='ru', reversed=True)

    ean = Code39(article, writer=CustomWriter(title), add_checksum=False)
    name = ean.save(f'media/barcode.png',
                    options={"module_width": 0.1, "module_height": 8, "font_size": 14, "text_distance": 1,
                             "quiet_zone": 3})
    # resize_image(f'{article}.png', 60, 40)