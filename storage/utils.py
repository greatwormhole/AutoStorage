import os, io, base64
from PIL import Image, ImageDraw, ImageFont

def _img_to_bytestr(func):
    
    def decorator(*args, **kwargs):
        img = func(*args, **kwargs)
        with io.BytesIO() as output:
            img.save(output, format='PNG')
            return base64.b64encode(output.getvalue()).decode('ascii')
    
    return decorator

def create_img(message: str, bg_color: str = 'white', text_color: str = 'black', size: tuple = (600,  600), fontsize: int = 60, fontname: str = 'arial.ttf', safe: bool = False):
    W, H = size[0], size[1]
    _font = ImageFont.truetype(fontname, fontsize)
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), message, font=_font)
    draw.text(((W-w)/2, (H-h)/2), message, font=_font, fill=text_color)
    if safe:
        img.save(f'media/{message}.png', 'PNG')
    return img

@_img_to_bytestr
def fast_convert(message: str, *args, **kwargs):
    return create_img(message, *args, **kwargs)

create_img('Crate#0000101', safe=True)
create_img('Crate#0000102', safe=True)