import mysql.connector
from mysql.connector import errorcode
import json
import os
 
# MYSQL CONFIG VARIABLES
hostname    = "localhost"
username    = "zaheer"
passwd  = "Secretpassword"
db = "TEST_DB"

def getConnection():    
    try:
        conn = mysql.connector.connect(host=hostname,                              
                              user=username,
                              password=passwd,
                              database=db)  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:  
        return conn   
    


DATA_FILE = 'users.json'

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)
                
