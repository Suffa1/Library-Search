import os
from flask import Flask, render_template, request, abort, url_for, session, redirect
import os # Make sure os is imported for getenv to work

app = Flask(__name__)
app.secret_key = 'any_random_string_here' # Required to encrypt the session cookie

app.config['username'] = os.getenv('username')
app.config['password'] = os.getenv('password')


@app.route('/')
def hello():
    # Check if the user is actually logged in
    if not session.get('logged_in'):
        return redirect(url_for('index')) # Send them back to login page
        
    return render_template('home.html')

@app.route('/login')
def index():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
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
        return abort(401)

if __name__ == '__main__':
    app.run(debug = True, port=9000)