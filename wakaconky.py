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

