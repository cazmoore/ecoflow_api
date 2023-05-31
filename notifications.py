import config
import requests

PUSHOVER_TOKEN = config.PUSHOVER_TOKEN
PUSHOVER_USER_TOKEN = config.PUSHOVER_USER_TOKEN


def send_push_notification(message, title):
    message = message
    url = 'https://api.pushover.net/1/messages.json'
    title = title
    my_pushover_request = {'token': PUSHOVER_TOKEN, 'user': PUSHOVER_USER_TOKEN,
                           'title': title, 'message': message}
    requests.post(url, data=my_pushover_request)
