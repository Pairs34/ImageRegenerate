import datetime
import json
from email.mime.image import MIMEImage
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw
from reportlab.pdfgen import canvas

from mail import Mail

mail = Mail()


def fill_color(image: Image, color: tuple, **kwargs):
    for x in range(kwargs["xstart"], kwargs["xend"]):
        for y in range(kwargs["ystart"], kwargs["yend"]):
            image.putpixel((x, y), color)


def add_text(image: Image, text, position, text_color, font_size=14, bold_offset=2):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("droid.ttf", font_size)

    if bold_offset == 0:
        draw.text(position, text, font=font, fill=text_color)
    else:
        for offset in range(bold_offset):
            draw.text((position[0] + offset, position[1]), text, font=font, fill=text_color)


def load_cards():
    f = open("cards.json", "r", encoding="utf-8-sig")
    veri = json.load(f, strict=False)

    return veri["cards"]


def create_pdf_from_image(image_path: str):
    img = Image.open(image_path)
    width, height = img.size
    pdf_stream = BytesIO()
    c = canvas.Canvas(pdf_stream, pagesize=(width, height))
    c.drawImage(image_path, 0, 0, width, height)
    c.save()
    pdf_stream.seek(0)
    return pdf_stream


white_color = (255, 255, 255)
red_color = (255, 0, 0)
black_color = (0, 0, 0)

cards = load_cards()

for card in cards:
    print(card["cardnumber"])
    image = Image.open("base.png")
    add_text(image, card["cardnumber"], (722, 1060), black_color, 27, bold_offset=1)
    add_text(image, f'{str(card["price"])} TL', (722, 1100), black_color, 27, bold_offset=1)
    date_now_more_60_days = (datetime.datetime.now() + datetime.timedelta(days=60)).strftime('%d/%m/%Y')
    add_text(image, date_now_more_60_days, (722, 1152), black_color, 27, bold_offset=1)
    image.save(f"cards/{card['cardnumber']}.png")

    attachment = create_pdf_from_image(f"cards/{card['cardnumber']}.png")

    resim_mime = MIMEImage(attachment.read(), _subtype='pdf')
    resim_mime.add_header('Content-Disposition', 'attachment', filename=f'{str(card["cardnumber"])}.pdf')

    mail.send_mail("omur.ilgit.inak@gmail.com",
                   "botsepeti@gmail.com",
                   "İnsan Kaynakları",
                   "",
                   "Kurumsal Hediye Çekiniz",
                   resim_mime)


