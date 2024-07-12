import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

BASE_URL = "https://api.github.com/search/code?q="


def code_search(query):
    url = BASE_URL + query
    response = requests.post(url, headers=headers)
    return response.json()