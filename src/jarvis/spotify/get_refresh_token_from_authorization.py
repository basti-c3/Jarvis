import base64
import os

import requests
from dotenv import load_dotenv

from paths import spotify_token_url, spotify_redirect_url
from shared.utils import Warn


def get_refresh_token_from_authorization(authorization_code):
    if authorization_code is None or authorization_code == "":
        raise Exception("Error in get_refresh_token_from_authorization: Please provide an authorization_code")
    load_dotenv()
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    request_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": spotify_redirect_url
    }

    request_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the POST request to the token endpoint
    response = requests.post(spotify_token_url, headers=request_headers, data=request_data)
    if response.status_code == 200:
        refresh_token = response.json().get('refresh_token')
        update_env_file(refresh_token, 'SPOTIFY_REFRESH_TOKEN')
        print("Successfully updated the refresh_token! You can now start the application")
    else:
        Warn(
            f"Error in get_refresh_token_from_authorization: Failed to get refresh token, status: {response.status_code}, {response.json()}")


def update_env_file(token, token_name):
    # Path to your .env file
    env_file = '../../../.env'

    # Load existing environment variables
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value

    # Update or add the SPOTIFY_REFRESH_TOKEN
    env_vars[token_name] = token

    # Write back to the .env file
    with open(env_file, 'w') as file:
        for key, value in env_vars.items():
            file.write(f'{key}={value}\n')


if __name__ == "__main__":
    authorization_code = "abc"
    get_refresh_token_from_authorization(authorization_code)
