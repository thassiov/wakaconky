#!/usr/bin/python3

import os
import json
import datetime
import requests

def getAccessTokenFromFile():
    """gets the api's access token from ~/.wakaconky 
    :returns: string

    """
    configFile = os.path.expanduser('~/.wakatime.cfg')

    try:
        c = open(configFile)
    except (OSError, IOError) as e:
        if e.errno == 2:
            return ''
        else:
            raise e

    for line in c:
        if 'api_key' in line :
            token = line.split(' ')[2]
            return token
    return ''

def getSummary(token):
    """get the user's summary from wakatime
    :returns: json

    """
    today = datetime.datetime.now()
    startTime = today.strftime('%Y-%m-%d')
    params = {'start':startTime, 'end':startTime, 'api_key':token} 

    headers = {'Accept':'application/x-www-form-urlencoded'}
    api_route = 'https://wakatime.com/api/v1/users/current/summaries'
    r = requests.get(api_route, headers=headers, params=params)
    return r.json()

token = getAccessTokenFromFile()
if token == '':
    print('api key needed!')
else:
    data = getSummary(token)
    print(data["data"][0]["grand_total"]["text"])

