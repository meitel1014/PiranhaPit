#coding:utf-8

import requests
import json
import os
from requests_oauthlib import OAuth1Session


#timerには次回起動時にナワバリショッツルが何時間後に終わるかを記述してある
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


def overwrite(file, timer):
    file.seek(0)
    file.write(str(timer))
    file.truncate()


def tweet():
    tweet = ""
    with open('timer.txt', 'r+') as file:
        timer = int(file.read())
        if timer == -1:
            next = getSchedule()
            if next == -1:
                tweet = "おっ、ナワバリショッツルないやんけ。"
            else:
                tweet = "おっ、" + str(next - 2) + "時間後ナワバリショッツルやんけ。"
                overwrite(file, next - 1)
        elif timer == 0:
            tweet = "おっ、ナワバリショッツル終わったやんけ。"
            overwrite(file, getSchedule() - 1)
        elif timer == 1 or timer == 2:
            tweet = "おっ、ナワバリショッツルやんけ。"
            overwrite(file, timer - 1)
        else:
            tweet = "おっ、" + str(timer - 2) + "時間後ナワバリショッツルやんけ。"
            overwrite(file, timer - 1)

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
    tweet()
