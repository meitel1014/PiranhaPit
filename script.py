#coding:utf-8

import requests
import json
import os
from time import sleep
#from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests_oauthlib import OAuth1Session


#ナワバリショッツルが何時間後に終わるかを返す
def getSchedule():
    url = 'https://spla2.yuu26.com/regular/schedule'
    headers = {'User-Agent': 'MEITEL twitter@meitel1014'}
    response = requests.get(url, headers=headers)
    schedule = response.json()

    hour = 0
    for result in schedule["result"]:
        hour += 2
        for map_data in result["maps_ex"]:
            if map_data["id"] == 17:
                return hour

    return -1


#毎50分に起動する
def tweet():
    tweet = ""

    next = getSchedule()
    if next == -1:
        tweet = "おっ、ナワバリショッツルないやんけ。"
    elif next == 2:
        if datetime.now().hour % 2 == 0:
            tweet = "おっ、ナワバリショッツル終わったやんけ。"
        else:
            tweet = "おっ、ナワバリショッツルやんけ。"
    elif next == 4:
        if datetime.now().hour % 2 == 0:
            tweet = "おっ、ナワバリショッツルやんけ。"
        else:
            tweet = "おっ、" + 1 + "時間後ナワバリショッツルやんけ。"
    else:
        if datetime.now().hour % 2 == 0:
            tweet = "おっ、" + str(next - 4) + "時間後ナワバリショッツルやんけ。"
        else:
            tweet = "おっ、" + str(next - 3) + "時間後ナワバリショッツルやんけ。"

    now = datetime.now()
    nexthour = now + timedelta(hours=1)
    tweettime = datetime(nexthour.year, nexthour.month, nexthour.day,
                         nexthour.hour, 0, 0)
    sleep((tweettime - now).total_seconds())

    if next == -1:
        nexnext = getSchedule()
        if nexnext != -1:
            tweet = "おっ、" + str(next - 2) + "時間後ナワバリショッツルやんけ。"
    print(tweet)

    twitter = OAuth1Session(
        os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"],
        os.environ["ACCESS_TOKEN_KEY"], os.environ["ACCESS_TOKEN_SECRET"])

    twparams = {"status": tweet}
    req = twitter.post(
        "https://api.twitter.com/1.1/statuses/update.json", params=twparams)

    if req.status_code == 200:  #正常投稿出来た場合
        print("Success.")
    else:  #正常投稿出来なかった場合
        print("Failed. : %d" % req.status_code)


if __name__ == "__main__":
    #dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    #load_dotenv(dotenv_path)
    tweet()
