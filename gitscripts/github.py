#!/usr/bin/python3

import datetime
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

def getProject(username, token, projectName):
    """TODO: Docstring for getProject.
    :returns: TODO

    """
    url = 'https://api.github.com/repos/' + projectName
    r = requests.get(url, auth=(username, token))
    return r.json()

def getAllIssues(userinfo):
    """TODO: Docstring for getAllIssues.

    :userinfo: TODO
    :returns: TODO

    """
    gh = getGithubIssues(userinfo["github_username"], userinfo["github_token"])

    projectsFullNames = set()
    for issue in gh:
        projectsFullNames.add(issue["repository"]["full_name"])

    projectsNamesAndUpdates = {}
    for name in projectsFullNames:
        p = getProject(userinfo["github_username"], userinfo["github_token"], name)
        lastActivity = datetime.datetime.strptime(p["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
        projectsNamesAndUpdates.update({p["id"]:{"path":p["full_name"], "last_activity":lastActivity.strftime("%A, %d. %B %Y %I:%M%p")}})

    print("\n>>> Github")
    for id in projectsNamesAndUpdates:
        print("[" + projectsNamesAndUpdates[id]["path"] + "] - Last activity: " + projectsNamesAndUpdates[id]["last_activity"])
        for issue in gh:
            if issue["repository"]["id"] == id:
                print(" ├─ #" + str(issue["number"]) + " - " + issue["title"])
        print(" └─────────────────")

getAllIssues(readConfigFile())
