import requests
import os
import pickle
import time
import procore_api_calls as pac
import json




def trade_authorization_code(client_id, client_secret, redirect_uri,login_url, auth_url_real):
    print(auth_url_real)
    authorization_code = input('paste authorization code:   ')
    fields = {'grant_type': 'authorization_code',
              "client_id": client_id,
              'client_secret': client_secret,
              'code': authorization_code,
              'redirect_uri': redirect_uri}

    response = requests.post(f'{login_url}/token', data=fields)
    print(response)
    # how to get a refresh token?
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']
    created_at = response.json()['created_at']
    expires_in = response.json()['expires_in']
    expiration = created_at + expires_in
    return access_token, refresh_token, expiration


def refresh_access_token(access_token, client_id, redirect_uri, client_secret, refresh_token, login_url_real):
    headers = {"Authorization": "Bearer " + access_token}
    # do the headers actually matter?
    data = {
    "grant_type":"refresh_token",
    "client_id": client_id,
    "client_secret":client_secret,
    "redirect_uri": redirect_uri,
    "refresh_token": refresh_token
}
    response = requests.post(f'{login_url_real}/token', data=data, headers=headers)
    response_json = response.json()
    access_token = response_json['access_token']
    refresh_token = response_json['refresh_token']
    created_at = response_json['created_at']
    expires_in = response_json['expires_in']
    expiration = created_at + expires_in

    return access_token, refresh_token, expiration


def is_access_token_expired(expiration):
    now = time.time()
    return now > expiration


def get_oauth_access():
    login_url_real = 'https://login.procore.com/oauth'
    base_url = 'https://api.procore.com'
    
    # Obtain cliend id and client secret by creating a Procore Developer Account
    # and following instructions to make your own App. www.procoredeveloper.com
    # you will need an admin on your Procore site to connect your app to the site.
    
    client_id_real = "YOUR CLIENT ID HERE"
    client_secret_real = "YOUR CLIENT SECRET HERE"
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    credentials_path = 'creds.pickle'
    auth_url_real = f'{login_url_real}/authorize?response_type=code&client_id={client_id_real}&redirect_uri={redirect_uri}'


    credentials = None
    # token.pickle stores the user credentials from previous successful logins
    if os.path.exists(credentials_path):
        print('Loading Credentials From File...')
        with open(credentials_path, 'rb') as token:  # rb stands for read bytes
            credentials = pickle.load(token)

    if credentials:
        if is_access_token_expired(credentials['expiration']):
            print('Refreshing Access Token...')

            access_token, refresh_token, expiration = refresh_access_token(credentials['access_token'], client_id_real, redirect_uri, client_secret_real, credentials['refresh_token'], login_url_real)

            credentials = {'access_token': access_token,
                           'refresh_token': refresh_token,
                           'expiration': expiration}

            with open(credentials_path, 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    elif not credentials:
        print("Fetching New Tokens...")

        access_token, refresh_token, expiration = trade_authorization_code(client_id_real, client_secret_real, redirect_uri, login_url_real, auth_url_real)

        credentials = {'access_token': access_token,
                       'refresh_token': refresh_token,
                       'expiration': expiration}

        with open(credentials_path, 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

    return credentials, base_url










