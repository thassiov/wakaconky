#!/usr/bin/python3

import datetime
import requests
import pprint
import os
import json

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

def getProject(token, projectid):
    """TODO: Docstring for getProject.

    :projectid: TODO
    :returns: TODO

    """
    url = 'https://gitlab.com/api/v4/projects/' + str(projectid)
    params = {'private_token': token}
    r = requests.get(url, params=params)
    return r.json()

def formatData(userinfo):
    """TODO: Docstring for getAllIssues.

    :userinfo: TODO
    :returns: TODO

    """
    gl = getGitlabIssues(userinfo["gitlab_token"])

    projectIds = set()
    for issue in gl:
        projectIds.add(issue["project_id"])

    projectIdAndName = {}
    for id in projectIds:
        p = getProject(userinfo["gitlab_token"], id)
        lastActivity = datetime.datetime.strptime(p["last_activity_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        projectIdAndName.update({id:{"path":p["path_with_namespace"], "last_activity":lastActivity.strftime("%A, %d. %B %Y %I:%M%p")}})

    print("\n>>> Gitlab")
    for id in projectIdAndName:
        print("[" + projectIdAndName[id]["path"] + "] - Last activity: " + projectIdAndName[id]["last_activity"])
        issueCount = 0
        # I need to show issues from 1 to 10, not from 10 to 1
        gl.reverse()
        for issue in gl:
            # 10 issues will be shown to save screen real state
            # @TODO 'issueCount' must be in a config file
            if issueCount == 10:
                break
            if issue["project_id"] == id:
                print(" ├─ #" + str(issue["iid"]) + " - " + issue["title"])
                issueCount +=1
                    
        print(" └─────────────────")

formatData(readConfigFile())
