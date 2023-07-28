import os, io, base64
from PIL import Image, ImageDraw, ImageFont

from Apro.settings import MEDIA_ROOT

def img_to_bytestr():
    ByteArrayIO = io.BytesIO()
    img = Image.open(os.path.join(MEDIA_ROOT, '123.jpg'))
    img.save(ByteArrayIO, format=img.format)
    res = base64.b64encode(ByteArrayIO.getvalue()).decode('ascii')
    return res

# def create_img(size: tuple, message: str, fontsize: int):
    
#     W, H = size[0], size[1]
#     _font = ImageFont.truetype('', 60)
#     img = Image.new('grayscale', size)
#     draw = ImageDraw.Draw(img)
#     _, _, w, h = draw.textbbox((0, 0), message, font=_font)
#     draw.text(((W-w)/2, (H-h)/2), message, font=_font, fill=fontColor)
#     return img