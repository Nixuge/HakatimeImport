import hashlib
import json
import os
from typing import cast
from rauth import OAuth2Service, OAuth2Session

SESS_CACHE_PATH = "cache/sess_cache.json"

def get_session():
    # print('Find your App Id at wakatime.com/apps')
    if os.path.exists(SESS_CACHE_PATH):
        session = get_session_cache()
    else:
        session = get_session_scratch()

    print('Getting current user from API...')
    user = session.get('users/current').json()
    print('Authenticated via OAuth as {0}'.format(user['data']['email']))
    print("Getting user's code stats from API...")

    return session

def get_session_cache():
    with open(SESS_CACHE_PATH) as f:
        d = json.load(f)
        client_id = d["client_id"]
        client_secret = d["client_secret"]
        token = d["token"]
    
    service = OAuth2Service(
        client_id=client_id,  # your App ID from https://wakatime.com/apps
        client_secret=client_secret,  # your App Secret from https://wakatime.com/apps
        name='wakatime',
        authorize_url='https://wakatime.com/oauth/authorize',
        access_token_url='https://wakatime.com/oauth/token',
        base_url='https://wakatime.com/api/v1/')

    return OAuth2Session(client_id, client_secret, token, service)


def get_session_scratch():
    client_id = input('Enter your App Id: ')
    client_secret = input('Enter your App Secret: ')

    service = OAuth2Service(
        client_id=client_id,  # your App ID from https://wakatime.com/apps
        client_secret=client_secret,  # your App Secret from https://wakatime.com/apps
        name='wakatime',
        authorize_url='https://wakatime.com/oauth/authorize',
        access_token_url='https://wakatime.com/oauth/token',
        base_url='https://wakatime.com/api/v1/')

    redirect_uri = 'https://wakatime.com/oauth/test'
    state = hashlib.sha1(os.urandom(40)).hexdigest()
    params = {'scope': 'email,read_stats.languages,read_heartbeats',
            'response_type': 'code',
            'state': state,
            'redirect_uri': redirect_uri}

    url = service.get_authorize_url(**params)

    print('**** Visit this url in your browser ****')
    print('*' * 80)
    print(url)
    print('*' * 80)
    print('**** After clicking Authorize, paste code here and press Enter ****')
    code = input('Enter code from url: ')

    # Make sure returned state has not changed for security reasons, and exchange
    # code for an Access Token.
    headers = {'Accept': 'application/x-www-form-urlencoded'}
    print('Getting an access token...')
    session = service.get_auth_session(headers=headers,
                                    data={'code': code,
                                            'grant_type': 'authorization_code',
                                            'redirect_uri': redirect_uri})

    session = cast(OAuth2Session, session)

    if input("Save the client_id, secret & token? (Y/n): ").lower() not in ["n", "no", "non"]:
        with open(SESS_CACHE_PATH, "w") as f:
            json.dump({"client_id": client_id, "client_secret": client_secret, "token": session.access_token}, f)
        print(f"You can change/clear the saved values by deleting the {SESS_CACHE_PATH} file.")

    return session