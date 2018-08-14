#coding:utf-8

import requests
import json

#import twitter


def getSchedule():
    url = 'https://spla2.yuu26.com/regular/schedule'
    headers = {'User-Agent': 'MEITEL twitter@meitel1014'}
    response = requests.get(url, headers=headers)
    schedule = response.json()

    hour = 0
    for result in schedule["result"]:
        for map_data in result["maps_ex"]:
            if map_data["id"] == 17:
                return hour
        hour += 2

    return -1


def overwrite(file, timer):
    file.seek(0)
    file.write(str(timer))
    file.truncate()


tweet = ""
with open('timer.txt', 'r+') as file:
    timer = int(file.read())
    if timer == -1:
        next = getSchedule()
        if next == -1:
            tweet = "おっ、ナワバリショッツルないやんけ。"
        else:
            tweet = "おっ、" + str(next) + "時間後ナワバリショッツルやんけ。"
            overwrite(file, next - 1)
    elif timer == 0:
        tweet = "おっ、ナワバリショッツル終わったやんけ。"
        overwrite(file, getSchedule() - 1)
    elif timer == 1 or timer == 2:
        tweet = "おっ、ナワバリショッツルやんけ。"
        overwrite(file, timer - 1)
    else:
        tweet = "おっ、" + str(timer) + "時間後ナワバリショッツルやんけ。"
        overwrite(file, timer - 1)

print(tweet)
