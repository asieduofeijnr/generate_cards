from PIL import Image, ImageDraw, ImageFont
import textwrap


class Cards:
    def __init__(self):
        pass

    def generate(self, message, color, pack):
        self.message = message
        self.color = color
        self.pack = pack

        if self.color == "black":
            text_fill_color = (255, 255, 255)
            logo = "Transparent_logo_black.png"
        if self.color == "white":
            text_fill_color = (0, 0, 0)
            logo = "Transparent_logo_white.png"

        height = 800
        width = 600

        signature = "Cards Against GoldCoast Politics"
        font = ImageFont.truetype("helveticaneuebd.ttf", size=65)
        signature_font = ImageFont.truetype("helveticaneue.ttf", size=20)
        img = Image.new("RGB", (width, height), color=self.color)

        text_position = (40, 40)
        signature_position = (100, 750)
        text_on_card = ImageDraw.Draw(img)
        signature_on_card = ImageDraw.Draw(img)

        if self.color == "white":
            border_color = (0, 0, 0)  # Black border for white cards
        if self.color == "black":
            border_color = (255, 255, 255)  # White border for black cards

        border_width = 1
        border_rect = [
            (border_width, border_width),
            (width - border_width, height - border_width),
        ]
        border_draw = ImageDraw.Draw(img)
        border_draw.rectangle(
            border_rect, outline=border_color, width=border_width)

        signature_on_card.text(
            signature_position, signature, font=signature_font, fill=text_fill_color
        )

        # Wrapped text
        line_width = 37
        line_height = 80
        wrapped_text = textwrap.wrap(
            self.message, width=int((600) / line_width))
        wrapped_text_height = len(wrapped_text) * (line_height)

        for line in wrapped_text:
            text_on_card.text(text_position, line, font=font,
                              fill=text_fill_color)
            text_position = (
                text_position[0],
                text_position[1] + line_height + 15,
            )  # Move to the next line

        # Load the small image to be inserted
        small_image = Image.open(logo)
        small_image_position = (40, 735)
        small_image_size = (50, 50)
        small_image = small_image.resize(small_image_size)
        img.paste(small_image, small_image_position)

        return img
