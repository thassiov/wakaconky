#!/usr/bin/python3

import os
import json
import datetime
import requests
import pprint

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
    route = 'https://wakatime.com/api/v1/users/current/summaries'
    return callWakatimeAPI(params, route)

def getStats(token):
    """get the user's stats for the last 7 days

    :token: string
    :returns: json

    """
    timeRange = 'last_7_days'
    params = {'api_key':token} 
    route = 'https://wakatime.com/api/v1/users/current/stats/' + timeRange
    return callWakatimeAPI(params, route)

def callWakatimeAPI(params, route):
    """handles the API requests

    :params: object
    :route: string
    :returns: json

    """
    headers = {'Accept':'application/x-www-form-urlencoded'}
    r = requests.get(route, headers=headers, params=params)
    return r.json()

def getWakatimeData(token):
    toBeStored = []

    summary = getSummary(token)
    toBeStored.append('time_spent_today = ' + summary["data"][0]["grand_total"]["text"]) # total
    minutes = int(summary["data"][0]["grand_total"]["total_seconds"])/60
    percent = minutes/(480/100) # 480 minutes = 8 hours
    percent = "{0:.2f}".format(percent)
    toBeStored.append('time_spent_today_as_percentage = ' + percent)

    langOfTheDay = summary["data"][0]["languages"][0]["name"]
    timeOnLangOfTheDay = summary["data"][0]["languages"][0]["text"]
    toBeStored.append('lang_of_the_day = ' + langOfTheDay)
    toBeStored.append('time_on_lang_of_the_day = ' + timeOnLangOfTheDay)

    last7days = getStats(token)
    bestDayInMinutes = int(last7days["data"]["best_day"]["total_seconds"])/60
    bestDayInMinutes = "{0:.2f}".format(bestDayInMinutes)
    bestDay = str(last7days["data"]["best_day"]["date"]) + ' - ' + str(bestDayInMinutes)
    toBeStored.append('best_day = ' + bestDay + ' mins')

    weekLang = last7days["data"]["languages"][0]["name"]
    weekLang += ' - ' + last7days["data"]["languages"][0]["text"]
    toBeStored.append("lang_of_the_week = " + weekLang)

    weekProj = last7days["data"]["projects"][0]["name"]
    weekProj += ' - ' + last7days["data"]["projects"][0]["text"]
    toBeStored.append("project_of_the_week = " + weekProj)

    username = last7days["data"]["username"]
    toBeStored.append("username = " + username)

    appendToWakaconkyData(toBeStored)

def wipeOldData():
    """erases wakaconky.data's content
    :returns: boolean

    """
    wkdata = os.path.expanduser('~/.wakaconky.data')
    try:
        open(wkdata, 'w').close()
    except (OSError, IOError) as e:
        print(e)
        return False
    return True

def appendToWakaconkyData(toAppend):
    dataFile = os.path.expanduser('~/.wakaconky.data')
    try:
        f = open(dataFile, 'a')
    except Exception as e:
        raise e

    for dataChunk in toAppend:
        f.write(dataChunk)
        f.write('\n')
    f.close()
    return True

token = getAccessTokenFromFile()
if token == '':
    print('api key needed!')
else:
    wipeOldData()
    getWakatimeData(token)
