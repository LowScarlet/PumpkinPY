import mysql.connector
import hashlib
import json
import os
#
def Hash(raw, hash):
    hash_parts = hash.split("$");alg, salt, digest = hash_parts[1:];a = hashlib.sha256(hashlib.sha256(raw.encode()).hexdigest().encode() + salt.encode());final_hash = f"${alg}${salt}${a.hexdigest()}"
    return final_hash
#
if os.path.exists('mysql.json'):
    with open('mysql.json', 'r') as openfile:
        mysqlData = json.load(openfile)
else:
    mysqlData = {"host":"type-here",
                 "user":"type-here",
                 "password":"type-here",
                 "database":"type-here"
                }
    with open('mysql.json', 'w') as outfile:  
        json.dump(mysqlData, outfile)
try:
    mydb = mysql.connector.connect(host=mysqlData["host"],user=mysqlData["user"],password=mysqlData["password"],database=mysqlData["database"])
except:
    print("[ERROR] Unable to login to mysql!")
# The Function
def checkPassword(username,password):
  try:
    mycursor = mydb.cursor();mycursor.execute("SELECT password FROM authme WHERE username ='"+username+"'");myresult = mycursor.fetchall();myresult = str(myresult);myresult = myresult.split("'")
    if Hash(password, myresult[1]) == myresult[1]:
        return True
    return False
  except:
    return False
