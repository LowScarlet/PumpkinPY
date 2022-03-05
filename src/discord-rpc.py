import os
import time

import requests
from pypresence import Presence

url = "http://sg-1.leyzstore.net:25573"
rpc = Presence("890789468150329414")

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def getDataPlayer(player):
    response = requests.get(url+"/playerapi?get="+player)
    data = response.json()
    return data

def getDataWorld(w):
    response = requests.get(url+f"/serverapi?get=world&value={w}")
    data = response.json()
    return data

def login():
    player = input("Nickname: ")
    password = input("Password: ")
    response = requests.get(url+f"/authme?nickname={player}&password={password}")
    if response.json()["status"] == True:
        clearConsole()
        start(player)
    else:
        print("Password salah!")

def start(player):
    rpc.connect()
    while True:
        data = getDataPlayer(player)
        
        detail = f"Login as {data['nickname']}"
        if data["status"] == "online":
            groupname = getDataWorld(data["current-world"])["displayname"]
            status = f"Playing in {groupname}"
            lastlog = int(data["lastlogin"])
            s_img = "green_circle"
            s_txt = "Online"
        else:
            status = data["status"].title()
            lastlog = None
            s_img = "red_circle"
            s_txt = "Offline"

        rpc.update(
            details=detail,
            state=f" - {status}",
            large_image="icon",
            start=lastlog,
            small_image=s_img,
            small_text=s_txt,
            # large_text="@pumpkinProject: Pumpkincraft"
            buttons=[
                    {"label": "Join", "url": "http://mc.pumpkinproject-id.com"},
                    {"label": "Discord Community", "url": "https://discord.gg/UYhQCqUj6F"}
                  ]
        )
        time.sleep(1)

login()
