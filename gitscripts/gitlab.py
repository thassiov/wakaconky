#!/usr/bin/python3

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
        projectIdAndName.update({id:p["path_with_namespace"]})

    print("\n>>> Gitlab")
    for issue in gl:
        print("["+ projectIdAndName[issue["project_id"]] +"] #" + str(issue["iid"]) + " - " + issue["title"])

formatData(readConfigFile())
