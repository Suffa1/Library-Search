import os
from flask import Flask, render_template, request, abort, url_for
app = Flask(__name__)

app.config['username'] = os.getenv('username')
app.config['password'] = os.getenv('password')

@app.route('/')
def hello():

    return render_template('home.html')

@app.route('/login')
def index():

    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def result():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == app.config['username'] and password == app.config['password']:
        return "login successfuly"
    else:
        return abort(401)

if __name__ == '__main__':
    app.run(debug = True, port=9000)