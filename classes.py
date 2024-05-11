import pandas as pd
import streamlit as st
import requests
import smtplib
import time
import json
import os

from json.decoder import JSONDecodeError
from google.cloud import bigquery
from prompt import *
from openai import OpenAI

from email.mime.text import MIMEText


class Data:
    def __init__(self, attribute, filepath):
        self.attribite = attribute
        self.filepath = filepath
        pass

    def to_file(self, message):
        with open(self.filepath, self.attribite) as file:
            file.writelines(message)

    def read_file(self):
        with open(self.filepath, self.attribite) as file:
            card_texts = file.readlines()
        return card_texts

    def read_json(self):
        with open(self.filepath, self.attribite) as file:
            card_texts = json.load(file)
        return card_texts


class Api:
    def __init__(self, type):
        self.type = type
        self.url = f"https://restagainsthumanity.com/api/v2/{self.type}"
        pass

    def generate(self, packs, color, pick):
        self.packs = packs
        self.color = color
        self.pick = pick

        params = {"packs": self.packs, "color": self.color, "pick": self.pick}
        response = requests.get(self.url, params=params)
        response = response.json()
        return response


# ---------------------------------------------------------------------

# Openai Key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# chat GPT Function
def chat_gpt_query(prmpt_system, prmpt_user_1, prmpt_assistant, random_black, random_white, context):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prmpt_system},
            {"role": "user", "content": prmpt_user_1},
            {"role": "assistant", "content": prmpt_assistant},
            {"role": "user", "content": f"EXAMPLE BLACK CARDS : {random_black}, EXAMPLE WHITE CARDS : {random_white}, Context : {context}"}]
    )

    result = response.choices[0].message.content
    return result


# Remove api key account
def google_client():
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'akronomacloudserviceaccount.json'
    st.secrets['akronomacloudserviceaccount']
    client = bigquery.Client()
    return client


def upload_to_bigquery(client, table_id, data):

    errors = client.insert_rows_json(table_id, data)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def parse_json(json_string):
    try:
        return json.loads(json_string)
    except JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {"Generated_Black_Cards": [],
                "Generated_White_Cards": []}


def merged_cards(df, column):
    merged_list_black = []
    merged_list_white = []
    for entry in df[column]:
        generated_card_dict = parse_json(entry)
        merged_list_black.extend(generated_card_dict["Generated_Black_Cards"])
        merged_list_white.extend(generated_card_dict["Generated_White_Cards"])
    return merged_list_black, merged_list_white


def sentences_to_json(card_list, color, category=None):
    json_data = []
    for sentence in card_list:
        if len(sentence) <= 90:
            if color == "white":
                entry = {
                    "text": sentence,
                    "pack": f"Ghana CAH {category}" if category else "Ghana CAH",
                    "color": color
                }
            else:
                entry = {
                    "text": sentence,
                    "pack": f"Ghana CAH {category}" if category else "Ghana CAH",
                    "pick": sentence.count("_"),
                    "color": color
                }
            json_data.append(entry)
    return json_data


def generated_cards_for_upload(json_file):
    columns = ['Date', 'category', 'text', 'pack', 'pick', 'color']
    formatted_data = []
    for entry in json_file:
        formatted_entry = {col: entry.get(col, None) for col in columns}
        formatted_data.append(formatted_entry)
    return formatted_data


def email_sender(subject, body, recipient_email):
    sender_email = "adwintechnology@gmail.com"  # replace with your email
    # replace with your password
    sender_password = os.getenv('GMAIL_ADWIN_PASSWORD')

    try:
        # Set up server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server_ssl:
            # Log in to the server
            server_ssl.login(sender_email, sender_password)

            # Prepare email
            message = MIMEText(body, 'plain')
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            # Send email
            server_ssl.send_message(message)
            print("Email sent successfully!")

    except Exception as e:
        print(f'Something went wrong... {e}')


# Function to check if the cache file needs updating
def is_data_updated(file_path, max_file_age_hours=24):
    if not os.path.exists(file_path):
        return False  # File does not exist, need to update
    file_mod_time = os.path.getmtime(file_path)
    current_time = time.time()
    # Check if the file is older than the max allowed age
    if (current_time - file_mod_time) / 3600 > max_file_age_hours:
        return False  # Data is old, needs to be updated
    return True


def get_data(file_path, state):
    cache_file_path = file_path

    if state:
        # Load data from the cache file
        df = pd.read_csv(cache_file_path)
    else:
        # Data needs to be updated
        client = google_client()
        QUERY = (
            "SELECT text,pack,pick,color FROM `akronoma.NewsScraping.Generated_Cards`"
        )

        query_job = client.query(QUERY)
        rows = query_job.result()

        # Gather data into a list of dictionaries
        generated_card_df = [
            {'text': row.text, 'pack': row.pack,
                'pick': row.pick, 'color': row.color}
            for row in rows
        ]

        df = pd.DataFrame(generated_card_df)
        # Save updated data to cache file
        df.to_csv(cache_file_path, index=False)

    return df
