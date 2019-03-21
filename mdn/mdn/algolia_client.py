import json
import os

from algoliasearch import algoliasearch
from dotenv import find_dotenv, load_dotenv


def get_algolia_client():
    load_dotenv(find_dotenv())
    app_id = os.getenv('APP_ID')
    api_key_admin = os.getenv('API_KEY_ADMIN')
    return algoliasearch.Client(app_id, api_key_admin)


def push_to_algolia():
    client = get_algolia_client()
    index = client.init_index('css')
    index.add_objects(json.load(open('data.json')))
