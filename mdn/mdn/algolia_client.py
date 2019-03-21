import json
import os

from algoliasearch import algoliasearch
from dotenv import find_dotenv, load_dotenv
from loguru import logger


def get_algolia_index():
    load_dotenv(find_dotenv())
    app_id = os.getenv('APP_ID')
    api_key_admin = os.getenv('API_KEY_ADMIN')
    client = algoliasearch.Client(app_id, api_key_admin)
    return client.init_index('css')


def check_index_not_populated():
    index = get_algolia_index()
    if index.search('')['nbHits'] > 0:
        exit('data already pushed to Algolia, bailing out 🛶')


def push_to_algolia():
    index = get_algolia_index()
    index.add_objects(json.load(open('data.json')))
    logger.debug('writing data to algolia 📡')
