#!/usr/bin/python3

import os
import hashlib
import sys
from rauth import OAuth2Service

def getAccessTokenFromFile():
    """gets the api's access token from ~/.wakaconky 
    :returns: string

    """
    configFile = os.path.expanduser('~/.wakaconky')

    try:
        c = open(configFile)
    except (OSError, IOError) as e:
        if e.errno == 2:
            return ''
        else:
            raise e

    for line in c:
        if 'access_token' in line :
            token = line.split(' ')[2]
            return token
    return ''

def makeNewAccessToken():
    """yeah. code from [https://wakatime.com/developers#authentication]
    :returns: string

    """
    client_id = input('Enter your App Id: ')
    secret = input('Enter your App Secret: ')

    service = OAuth2Service(
        client_id=client_id, # your App ID from https://wakatime.com/apps
        client_secret=secret, # your App Secret from https://wakatime.com/apps
        name='wakatime',
        authorize_url='https://wakatime.com/oauth/authorize',
        access_token_url='https://wakatime.com/oauth/token',
        base_url='https://wakatime.com/api/v1/')

    redirect_uri = 'https://wakatime.com/oauth/test'
    state = hashlib.sha1(os.urandom(40)).hexdigest()
    params = {'scope': 'email,read_stats',
              'response_type': 'code',
              'state': state,
              'redirect_uri': redirect_uri}

    url = service.get_authorize_url(**params)

    print('**** Visit {url} in your browser. ****'.format(url=url))
    print('**** After clicking Authorize, paste code here and press Enter ****')
    code = input('Enter code from url: ')
    return code

