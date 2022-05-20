import json
from stackapi import StackAPI

def get_site():
    with open('secrets.json', 'r') as raw_secrets:
        secrets = json.load(raw_secrets)
        key = secrets.get('key')
        access_token = secrets.get('access_token')
    SITE = StackAPI('stackoverflow', key=key, access_token=access_token)
    return SITE

def test_connection():
    SITE = get_site()
    response = SITE.fetch('me')
    print(response)