from bottle import Bottle, request
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Bottle()


def start_server(host, port):
    logger.debug('running server')
    app.run(host=host, port=port)


@app.post('/trellocallbacks')
def webhook_callback():
    logger.debug('callback triggered')
    logger.debug(request.json)
    return


@app.get('/')
def home():
    logger.debug('home triggered')
    return 'PCOTrello server is up'


if __name__ == '__main__':
    start_server('localhost', 8080)
