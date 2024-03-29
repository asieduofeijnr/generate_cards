from manipulate_data_class import Data
from card_generator_class import Cards
import pandas as pd
import random
import streamlit as st
import io

st.set_page_config(page_title="GoldCoast CAH", page_icon="Transparent_logo_white.png")

col1, col2 = st.columns([1, 3])
col1.image(image="Transparent_logo_white.png", width=150)
col2.title("Cards Against GoldCoast Politics")

st.button(label="TAP ME FOR A SHUFFLE")

FILEPATH = "gtp_samples.json"


read_cards = Data(attribute="r", filepath=FILEPATH)
card_text = read_cards.read_json()
df = pd.DataFrame(card_text)

packs = df.pack.unique()
card_pack = packs[random.randint(0, len(packs) - 1)]
rand_pack_black = df.loc[(df["pack"] == card_pack) & (df["color"] == "black")]
rand_pack_white = df.loc[(df["pack"] == card_pack) & (df["color"] == "white")]

# Black Card
black_card = rand_pack_black.sample()
black_card_message = str(black_card["text"].squeeze())
black_card_pack = str(black_card["pack"].squeeze())
black_card_color = str(black_card["color"].squeeze())


# generate card image
blackCard = Cards()
whiteCard = Cards()

# 1 Random Black Card
black_img = blackCard.generate(
    message=black_card_message, color=black_card_color, pack=black_card_pack
)

# Convert black card image to bytes
black_img_bytes = io.BytesIO()
black_img.save(black_img_bytes, format="PNG")
st.image(black_img_bytes.getvalue(), width=300)

st.subheader(
    "Fill in the blank :top: in the black card with the text from any of the white cards and it will turn the goldcoasts awkward personality into hours of fun."
)
# 7 Random White Cards2
img_bytes = []
for card in range(0, 5):
    white_card = rand_pack_white.sample()
    white_card_message = str(white_card["text"].squeeze())
    white_card_pack = str(white_card["pack"].squeeze())
    white_card_color = str(white_card["color"].squeeze())
    white_img = whiteCard.generate(
        message=white_card_message, color=white_card_color, pack=white_card_pack
    )
    white_img_bytes = f"{img_bytes}{card}"
    white_img_bytes = io.BytesIO()
    img_bytes.append(white_img_bytes)
    white_img.save(white_img_bytes, format="PNG")


white0, white1 = st.columns(2)
white0.image(img_bytes[0].getvalue(), width=300)
white1.image(img_bytes[1].getvalue(), width=300)

white2, white3 = st.columns(2)
white2.image(img_bytes[2].getvalue(), width=300)
white3.image(img_bytes[3].getvalue(), width=300)

st.image(img_bytes[4].getvalue(), width=300)

st.subheader(
    "This is a modification of the original game 'Cards Against Humanity' and is created under the Creative Commons BY-NC-SA 2.0 License. Please visit https://creativecommons.org/licenses/by-nc-sa/2.0/ "
)
st.subheader("Get the original game at https://www.cardsagainsthumanity.com/")

st.write("NoBadDays|TheGoodLife")
