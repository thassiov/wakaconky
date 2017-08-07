#!/usr/bin/python3

import os

def getAccessTokenFromFile():
    """gets the api's access token from ~/.wakaconky 
    :returns: string

    """
    configFile = os.path.expanduser('~/.wakaconky')
    with open(configFile) as c:
        for line in c:
            if 'access_token' in line :
                token = line.split(' ')[2]
                return token
        return ''
