import pytest
import logging.config
import requests
import json

from time import sleep
from threading import Thread

from pcotrello.server import start_server
from pcotrello.pcotrello import setup_webhook

logger = logging.getLogger(__name__)
logging.config.fileConfig('../logging.ini', disable_existing_loggers=False)

# TODO: Make this environvars
HOST = 'localhost'
PORT = 8080
TEST_SERVER_URL = f'http://{HOST}:{PORT}/'


@pytest.fixture(scope='session', autouse=True)
def start_server_in_thread():
    server_thread = Thread(target=start_server, args=(HOST, PORT),
                           daemon=True)
    server_thread.start()
    # Give the server a chance to set up on the port otherwise can get errno 111
    sleep(1)
    yield


def test_null():
    assert True


def test_home():
    response = requests.get(TEST_SERVER_URL)
    logger.info(response)
    logger.info(response.text)
    assert response.status_code == requests.codes.ok
    assert response.text == 'PCOTrello server is up'


def test_webhook_response():
    with open('webhook_action.json', 'r') as input_data:
        response = requests.post(TEST_SERVER_URL + 'trellocallbacks',
                                 json=json.load(input_data))
    logger.debug(response)
    logger.debug(response.text)
    assert response.status_code == requests.codes.ok
