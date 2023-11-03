import json
import os
import base64


SECRET_PATH = os.path.dirname(os.path.abspath(__file__))


def get_secrets(key):
    secrets = json.loads(open(os.path.join(SECRET_PATH, 'secrets.json')).read())
    return secrets[key]
