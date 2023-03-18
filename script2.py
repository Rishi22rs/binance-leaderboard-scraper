import requests
import time
import sys
import os


url='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'
urlForName='https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo'
headers= {
    "content-type": "application/json",
    "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
    "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
}

sleepTime=10

data=[]

backupData=[]

closed=[]
opened=[]

f=True

def getSelectedUserData(idx,name):
    global backupData
    global f
    req=requests.post(url,headers=headers,json={
        "encryptedUid": sys.argv[idx],
        "tradeType": "PERPETUAL"
    }).json()

    if(len(backupData)>0):
        for position in backupData:
            if position not in req['data']['otherPositionRetList']:
                closed.append(position)

        for position in req['data']['otherPositionRetList']:
            if position not in backupData:
                opened.append(position)
    else:
        backupData=req['data']['otherPositionRetList']

    for id,item in enumerate(req['data']['otherPositionRetList']):
        symbol=item['symbol']
        amount=item['amount']
        entryPrice=item['entryPrice']
        leverage=item['leverage']
        markPrice=item['markPrice']
        pnl=item['pnl']
        roe=item['roe']
        print(f"{id+1}: {name}---{symbol}---Amount: {amount}\n\tEntry price: {entryPrice}\n\tLeverage: {leverage}\n\tMark price: {markPrice}\n\tPNL: {pnl}\n\tROE: {roe}")

def getSelectedUserName(idx):
    req=requests.post(urlForName,headers=headers,json={
        "encryptedUid": sys.argv[idx],
    }).json()
    getSelectedUserData(idx,req['data']['nickName'])

def getData():
    global opened
    global closed
    if(len(sys.argv)>1):
        print("Selected Users Data")
        for idx in range(1,len(sys.argv)):
            getSelectedUserName(idx)
            print("====================================")

        if(len(closed)>0 or len(opened)>0):
            print("Position changes")

        if len(opened)>0:
            print('Opened\n')
        
        for idx,o in enumerate(opened):
            symbol=o['symbol']
            amount=o['amount']
            entryPrice=o['entryPrice']
            leverage=o['leverage']
            markPrice=o['markPrice']
            pnl=o['pnl']
            roe=o['roe']
            print(f"{idx+1}: {symbol}---Amount: {amount}\n\tEntry price: {entryPrice}\n\tLeverage: {leverage}\n\tMark price: {markPrice}\n\tPNL: {pnl}\n\tROE: {roe}")
        
        opened=[]

        if len(closed)>0:
            print('Closed\n')

        for idx,c in enumerate(closed):
            symbol=c['symbol']
            amount=c['amount']
            entryPrice=c['entryPrice']
            leverage=c['leverage']
            markPrice=c['markPrice']
            pnl=c['pnl']
            roe=c['roe']
            print(f"{idx+1}: {symbol}---Amount: {amount}\n\tEntry price: {entryPrice}\n\tLeverage: {leverage}\n\tMark price: {markPrice}\n\tPNL: {pnl}\n\tROE: {roe}")
        
        closed=[]

    else:
        print("Please append users encryptedID while running the script.")

while(True):
    getData()
    time.sleep(sleepTime)
    os.system('cls')
    print('refreshing...')
    time.sleep(3)
    os.system('cls')