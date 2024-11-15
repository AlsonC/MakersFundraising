from openai import OpenAI
client = OpenAI()
import pandas as pd

# Load the Excel file
# file_path = "staff_data.xlsx"
# excel_data = pd.ExcelFile(file_path)

# OpenAI API key setup
OpenAI.api_key = 'sk-XGQ6l3gk32AVhaJiuAh-exnHT6Wr2zWOcQZ1J7HuwFT3BlbkFJj34e_k_-i61ie7QlnybQGjFcCzlpAN5ospFDkUrO8A'

file_path = r"C:\Users\theal\MakersFund\MakersFundraising\combined_staff_data_with_games.xlsx"
df = pd.read_excel(file_path)
df['games'] = None  # Add a new column 'games' with default value None

# For Testing
# df = df.head(10)


i = 0
def process_joined_value(value, cur_company, past_company_1, past_company_2):
    # Placeholder function to process the 'joined' column value
    # Replace this with the actual processing logic


    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Find a list of all the names of games that the person has worked on in the following text: {value}. Only return the list of games with a semicolon between each game, no other text. The games should be from the company {cur_company}, or previous companies {past_company_1} and {past_company_2}."
        }
        ]
    )
    return completion.choices[0].message.content

for index, row in df.iterrows():
    i += 1
    print(i)
    joined_value = row['joined']
    cur_company = row['current_company']
    past_company_1 = row['past_company_1']
    past_company_2 = row['past_company_2']
    processed_value = process_joined_value(joined_value, cur_company, past_company_1, past_company_2)
    df.at[index, 'games'] = processed_value


df.to_excel("updated_staff_data_with_games.xlsx", index=False)



