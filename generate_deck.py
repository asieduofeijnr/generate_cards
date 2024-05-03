from classes import *
import time


# Initialize Google BigQuery client
print('Initializing Google BigQuery client')
client = google_client()
table_id = "akronoma.NewsScraping.Generated_Cards"

# Empty list to store query results
generated_card_df = []

print('Querying BigQuery for News and Entertainment data')
# Define the SQL query
QUERY = (
    "SELECT PARSE_DATETIME('%c', date_time) AS Date,category_title, story_body "
    "FROM akronoma.NewsScraping.All_news "
    "WHERE category_title IN ('News', 'Entertainment') "
    "AND EXTRACT(MONTH FROM PARSE_DATETIME('%c', date_time)) = EXTRACT(MONTH FROM CURRENT_DATETIME())"
    "LIMIT 10"  # for testing purposes
)

# Execute the query
query_job = client.query(QUERY)
rows = query_job.result()


FILEPATH = "original_cards_dict.json"

read_cards = Data(attribute="r", filepath=FILEPATH)
card_text = read_cards.read_json()
card_df = pd.DataFrame(card_text)
rand_pack_black = card_df.loc[card_df["color"] == "black"]
rand_pack_white = card_df.loc[card_df["color"] == "white"]

random_black = [i for i in rand_pack_black.sample(3).text]
random_white = [i for i in rand_pack_white.sample(10).text]

print('Generating cards from News and Entertainment data using GPT-3')
# Iterate over the query results from big query and append them and generated card to the DataFrame
for count, row in enumerate(rows):
    generated_card_df.append({'Date_Time': row.Date, 'Category_title': row.category_title, 'Story_Body': row.story_body,
                             'Generated_cards': chat_gpt_query(prmpt_system, prmpt_user_1, prmpt_assistant, random_black, random_white, row.story_body)})
    print(f'Generated card {count + 1}')
    time.sleep(1)
print('Generated cards successfully')

final_df = pd.DataFrame(generated_card_df)
merged_list_black, merged_list_white = merged_cards(
    final_df, column='Generated_cards')
black_json = sentences_to_json(
    merged_list_black, color='black', category="News&Enterrtainment")
white_json = sentences_to_json(
    merged_list_white, color='white', category="News&Enterrtainment")
all_json = black_json + white_json

final_generated_cards = generated_cards_for_upload(all_json)

print('Uploading generated cards to BigQuery')
job = upload_to_bigquery(
    client=client, table_id=table_id, data=final_generated_cards)

subject = "CAH PROJECT"
body = f'''Done with uploading {len(final_generated_cards)} generated cards on {time.ctime(time.time())}
        BIGQUERY UPLOAD ERRORS -----> <<<{job}>>>'''
email_sender(subject, body, os.getenv('MY_EMAIL'))

print('Completed ----> Check your email for details')
