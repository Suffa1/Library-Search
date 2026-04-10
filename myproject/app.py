from flask import Flask, render_template, request, session, redirect, url_for, abort
from dbfunc import load_users # Import your librarian

app = Flask(__name__)
app.secret_key = 'momo_talk_secret'

@app.route('/')
def hello():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login_action', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    users = load_users()
    
    if username in users and users[username] == password:
        session['logged_in'] = True
        session['user'] = username
        return redirect(url_for('hello'))
    return abort(401)

# This line is important to connect the signup file later
import signup 

if __name__ == '__main__':
    app.run(debug=True, port=9000)