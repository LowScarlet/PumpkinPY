import numpy as np
import time
from uuid import uuid4
import threading
import datetime

database = "database.npy"
cache = "cache.npy"

def check():
    try:
        read_dictionary = np.load(database,allow_pickle='TRUE').item()
        return read_dictionary
    except:
        dictionary = {"admin":{"password":"admin","register-date":time.time(),"last-login":None}}
        np.save(database, dictionary)
        return dictionary

def isHaveRegister(username):
    read_dictionary = check()
    if username in read_dictionary:
        return True
    return False

def register(username,password):
    if not isHaveRegister(username):
        read_dictionary = check()
        read_dictionary[username] = {"password":password,"register-date":time.time(),"last-login":None}
        np.save(database, read_dictionary)
        return True
    else:
        return "username-is-taken"

def checkPassword(username,password):
    if isHaveRegister(username):
        read_dictionary = check()
        if read_dictionary[username]["password"] == password:
            return True
        return "password-incorrect"
    else:
        return "need-register-first"

def checkSessionTime():
    try:
        lastLogin = np.load(cache,allow_pickle='TRUE').item()["last-login"]
        s = datetime.datetime.utcfromtimestamp(time.time())-datetime.datetime.utcfromtimestamp(lastLogin)
        if int(s.seconds/60) > 2:
            breakLoginSession(currenctUsername())
            return "session-is-endded"
        return None
    except:
        return "no-last-login"

def loginSession(username):
    token = uuid4()
    cacheValue = {"username": username,"token": token,"last-login": time.time()}
    np.save(cache, cacheValue)
    dictionary = check()
    dictionary[username]["token"] = token
    dictionary[username]["last-login"] = time.time()
    np.save(database, dictionary)

def breakLoginSession(username):
    cacheValue = {"username":None,"token":None,"last-login": None}
    np.save(cache, cacheValue)
    dictionary = check()
    dictionary[username]["token"] = None
    np.save(database, dictionary)

def isLogin(username):
    try:
        read_userData = np.load(database,allow_pickle='TRUE').item()
        read_cacheData = np.load(cache,allow_pickle='TRUE').item()
        if read_userData[username]["token"] and read_cacheData["token"] != None:
            if read_userData[username]["token"] == read_cacheData["token"]:
                return True
            return False
        return False
    except:
        return False

def login(username,password):
    if checkPassword(username,password) == True:
        loginSession(username)
        return True
    return checkPassword(username,password)

def currenctUsername():
    try:
        read_cacheData = np.load(cache,allow_pickle='TRUE').item()
        return read_cacheData["username"]
    except:
        return None

def logout():
    if isLogin(currenctUsername()):
        breakLoginSession(currenctUsername())
        return True
    return "is-not-login"

debug = False
def whileDebug():
    while debug == True:
        if isLogin(currenctUsername()):
            print("IS-LOGIN")
        else:
            print("IS-NOT-LOGIN")
        time.sleep(1)

while True:
    print(checkSessionTime())
    if checkSessionTime() == "session-is-endded":
        print("Session login is endded!")
    command = input("Command: (register/login) ")
    if command == "register":
        username = input("Username:" )
        password = input("Password:" )
        if register(username,password) == True:
            print("Berhasil register dengan username",username)
        elif register(username,password) == "username-is-taken":
            print("Username sudah diambil!")
            
    elif command == "login":
        username = input("Username:" )
        password = input("Password:" )
        if login(username,password) == True:
            print("Success Login!")
        else:
            print(login(username,password))
            
    elif command == "islogin":
        print(isLogin(currenctUsername()))
            
    elif command == "logout":
        print(logout())
            
    elif command == "session":
        print(currenctUsername())
            
    elif command == "debug":
        if debug == True:
            debug = False
        else:
            debug = True
            threading.Thread(target=whileDebug).start()
            
    elif command == "checklastlogin":
        lastLogin = check()[currenctUsername()]["last-login"]
        if lastLogin != None:
            s = datetime.datetime.utcfromtimestamp(time.time())-datetime.datetime.utcfromtimestamp(lastLogin)
            print(int(s.seconds/60),"Minutes Ago")
            
    elif command == "checklastregister":
        lastLogin = check()[currenctUsername()]["register-date"]
        if lastLogin != None:
            s = datetime.datetime.utcfromtimestamp(time.time())-datetime.datetime.utcfromtimestamp(lastLogin)
            print(int(s.seconds/60),"Minutes Ago")


