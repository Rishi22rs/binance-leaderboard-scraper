import requests
import time
import sys
import os

url='https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank'
headers= {
    "content-type": "application/json",
    "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
    "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
}

payload = {
    "tradeType": "PERPETUAL",
    "statisticsType": "ROI",
    "periodType": "WEEKLY",
    "isShared": True,
    "isTrader": False
}

def getBinanceLeaderboard():
    while(True):
        req=requests.post(url,headers=headers,json=payload).json()
        print("Leaderboard")
        print("====================================")

        for idx,item in enumerate(req['data']):
            nickName=item["nickName"]
            encryptedUid=item["encryptedUid"]
            roi=item["roi"]
            print(f"{idx+1}: encrypted UID: {encryptedUid}\n\tName: {nickName}\n\troi: {roi}%")
        
        time.sleep(10)
        os.system('cls')
        print('refreshing...')
        time.sleep(3)
        os.system('cls')


getBinanceLeaderboard()
