#!/usr/bin/python3

import os
import datetime
import requests
import hashlib
import sys
import base64
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
    params = {'scope': 'email,read_stats,read_logged_time',
              'response_type': 'code',
              'state': state,
              'redirect_uri': redirect_uri}

    url = service.get_authorize_url(**params)

    print('**** Visit {url} in your browser. ****'.format(url=url))
    print('**** After clicking Authorize, paste code here and press Enter ****')
    code = input('Enter code from url: ')
    return code

def makeNewConfigFile(token):
    """creates a new config file with the APIs access token

    :token: string
    :returns: string

    """
    configFile = os.path.expanduser('~/.wakaconky')
    try:
        f = open(configFile, 'w')
    except Exception as e:
        raise e

    f.write('access_token = ' + token)
    f.close()
    return token

def getSummary(token):
    """get the user's summary from wakatime
    :returns: json

    """
    today = datetime.datetime.now()
    startTime = today.strftime('%Y-%m-%d')
    endTime = datetime.datetime.now() + datetime.timedelta(days=1)
    endTime = endTime.strftime('%Y-%m-%d')
    params = {'start':startTime, 'end':endTime, 'api_key':token} 

    headers = {'Accept':'application/x-www-form-urlencoded'}
    api_route = 'https://wakatime.com/api/v1/users/current/summaries'
    r = requests.get(api_route, headers=headers, params=params)
    return r.json()

token = getAccessTokenFromFile()
if token == '':
    newToken = makeNewAccessToken()
    token = makeNewConfigFile(newToken)

print(getSummary(token))
