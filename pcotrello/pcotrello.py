import json
import requests
import os
import logging

logger = logging.getLogger(__name__)


def main():
    logger.debug('Entering main')

    test_url = f'https://api.trello.com/1/boards/EnZlixMv' \
               f'?key={os.environ["TRELLO_API_KEY"]}' \
               f'&token={os.environ["TRELLO_API_SECRET"]}'

    response = requests.get(test_url)
    print(json.dumps(json.loads(response.text), indent=4))
    print(response)


def setup_webhook(model_id: str):
    url = f'https://api.trello.com/1/tokens/{os.environ["TRELLO_API_SECRET"]}' \
          f'/webhooks/?key={os.environ["TRELLO_API_KEY"]}'
    response = requests.post(
        url,
        data={'description': 'Test webhook',
              'callbackURL': 'http://192.168.122.1:8080/trellocallbacks',
              'idModel': model_id}
    )
    return response
