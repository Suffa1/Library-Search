from __main__ import app # Borrow the app from app.py
from flask import render_template, request, redirect, url_for
from dbfunc import load_users, save_user

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    users = load_users()
    if username in users:
        return "User already exists!", 400
    
    save_user(username, password)
    return redirect(url_for('login_page'))