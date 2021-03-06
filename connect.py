import requests
import json
from set_domain import domain


def get_token(email, password, security_code=''):
    try:
        token = requests.get(url=f'https://{domain}/api', json={'email': email, 'password': password,
                             'security_code': security_code}).content.decode()
        return token
    except:
        return False


def get_user_data(token):
    """Downloads user data json file and converts it to a dict."""
    try:
        response = requests.get(f'https://{domain}/api/{token}')
        data = json.loads(response.json())
        return data
    except:
        return False


def post_user_data(token, data):
    """Uploads a dict of encrypted user data or deletion request."""
    # dict template: data = {'action': 'add/edit/delete', 'data_type': 'password/secure_note/credit_card', 'data': data}
    try:
        response = requests.post(url=f'https://{domain}/api/{token}', json=data)
        return response
    except:
        return False
