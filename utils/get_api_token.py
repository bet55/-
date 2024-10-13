import os


def get_api_token():
    kp_api_token = os.environ.get('KP_API_TOKEN')
    return kp_api_token
