import mysql.connector
from mysql.connector import errorcode
import json
from flask import Flask, render_template, request, abort, url_for, session, redirect
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
    
def result():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == app.config['username'] and password == app.config['password']:
        # 1. Store the login status in the session
        session['logged_in'] = True
        session['user'] = username
        
        # 2. Redirect to the 'hello' function (the / route)
        return redirect(url_for('hello')) 
    else:
        return os.abort(401)
    


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