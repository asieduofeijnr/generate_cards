from PIL import Image, ImageDraw, ImageFont
import textwrap

card = {
    "text": "The Ghanaian version of 'Keeping up with the Kardashians' would feature _____",
    "pack": "CAH Base Set",
    "pick": 2,
    "color": "black",
}

height = 800
width = 600
corner_radius = 30

message = card["text"]
signature = "Cards Against Ghana Politics"
font = ImageFont.truetype("helveticaneuebd.ttf", size=65)
signature_font = ImageFont.truetype("helveticaneue.ttf", size=20)
img = Image.new("RGB", (width, height), color=card["color"])

text_position = (40, 40)
signature_position = (100, 750)
text_on_card = ImageDraw.Draw(img)
signature_on_card = ImageDraw.Draw(img)

signature_on_card.text(
    signature_position, signature, font=signature_font, fill=(255, 255, 255)
)

# Wrapped text
line_width, line_height = font.getsize("A")
wrapped_text = textwrap.wrap(message, width=int((800) / line_width))
wrapped_text_height = len(wrapped_text) * (line_height)

for line in wrapped_text:
    text_on_card.text(text_position, line, font=font, fill=(255, 255, 255))
    text_position = (
        text_position[0],
        text_position[1] + line_height + 30,
    )  # Move to the next line

# Load the small image to be inserted
small_image = Image.open("Transparent_logo.png")
small_image_position = (40, 735)
small_image_size = (50, 50)
small_image = small_image.resize(small_image_size)
img.paste(small_image, small_image_position)


img.save("result.png")
