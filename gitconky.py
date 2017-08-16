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

def getGitlabIssues(token):
    """get issues from the authenticated user
    :returns: TODO

    """
    url = 'https://gitlab.com/api/v4/issues?state=opened'
    params = {'private_token': token}
    r = requests.get(url, params=params)
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
    gl = getGitlabIssues(userinfo["gitlab_token"])

    print("Gitlab")
    for issue in gl:
        print(issue["title"])

    print("\nGithub")
    for issue in gh:
        print(issue["title"])

getAllIssues(readConfigFile())
