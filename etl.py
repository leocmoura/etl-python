import pandas as pd
import requests
import json
import os
from bardapi import Bard
from dotenv import load_dotenv


sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)


def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))


def generate_ai_news(user):
    load_dotenv()

    token = os.getenv('_BARD_API_KEY')
    bard = Bard(token=token)

    # prompt = f"Você é um especialista em marketing bancário. Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)."
    prompt = f"Me responda com apenas uma linha e no maximo 100 caracteres, crie uma frase para {user['name']} sobre a importancia dos investimentos, me retorne somente a frase."
    response = bard.get_answer(prompt)['content'].strip('\*')
    find = response.find('**')
    # print(response)
    response = response[:find]
    return response
    
for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")