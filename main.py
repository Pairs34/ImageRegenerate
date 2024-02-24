import json

from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw


def fill_color(image: Image, color: tuple, **kwargs):
    for x in range(kwargs["xstart"], kwargs["xend"]):
        for y in range(kwargs["ystart"], kwargs["yend"]):
            image.putpixel((x, y), color)


def add_text(image: Image, text, position, text_color, font_size=14, bold_offset=2):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("newsroman.ttf", font_size)

    if bold_offset == 0:
        draw.text(position, text, font=font, fill=text_color)
    else:
        for offset in range(bold_offset):
            draw.text((position[0] + offset, position[1]), text, font=font, fill=text_color)


def load_cards():
    f = open("cards.json", "r", encoding="utf-8-sig")
    veri = json.load(f, strict=False)

    return veri["cards"]


white_color = (255, 255, 255)
red_color = (255, 0, 0)
black_color = (0, 0, 0)

cards = load_cards()

for card in cards:
    print(card["cardnumber"])
    image = Image.open("base.png")

    fill_color(image, white_color, ystart=284, yend=324, xstart=602, xend=840)
    fill_color(image, white_color, ystart=344, yend=384, xstart=30, xend=339)
    fill_color(image, white_color, ystart=518, yend=548, xstart=891, xend=971)
    fill_color(image, white_color, ystart=670, yend=702, xstart=484, xend=770)
    add_text(image, "Ali YILDIRIM", (606, 293), black_color, 27, bold_offset=1)
    add_text(image, "  TK TUZLASHIPYARD", (35, 348), black_color, 30, bold_offset=1)
    add_text(image, str(card["price"]), (910, 516), black_color, 32, bold_offset=3)
    add_text(image, card["cardnumber"], (484, 670), black_color, 30, bold_offset=2)

    image.save(f"cards/{card['cardnumber']}.png")
