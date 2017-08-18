#!/usr/bin/python3

import requests
import pprint
import os
import json

def getGithubIssues(username, token):
    """gets issues from the authenticated user

    :token: TODO
    :returns: TODO

    """
    url = 'https://api.github.com/issues'
    r = requests.get(url, auth=(username, token))
    return r.json()

def readConfigFile():
    """TODO: Docstring for readConfigFile.
    :returns: TODO

    """
    configFile = os.path.expanduser("~/.gitconky.json")
    try:
        f = open(configFile)
    except (OSError, IOError) as e:
        if e.errno == 2:
            return ''
        else:
            raise e

    data = json.load(f)
    return data

def getAllIssues(userinfo):
    """TODO: Docstring for getAllIssues.

    :userinfo: TODO
    :returns: TODO

    """
    gh = getGithubIssues(userinfo["github_username"], userinfo["github_token"])


    print("\n>>> Github")
    for issue in gh:
        print("["+ issue["repository"]["full_name"] +"] #" + str(issue["number"]) + " - " + issue["title"])

getAllIssues(readConfigFile())
