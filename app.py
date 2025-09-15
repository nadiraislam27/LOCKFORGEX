from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

app = Flask(__name__)
# Use your provided secret key
app.secret_key = "84251379358517826681762094589523"

# MongoDB Atlas connection
MONGODB_URI = "mongodb+srv://lockforgex:556677889900@lockforgex.v4uoa2q.mongodb.net/lockforgex?retryWrites=true&w=majority&appName=lockforgex"
client = MongoClient(MONGODB_URI)
db = client.lockforgex
users_col = db.users
passwords_col = db.passwords

# 🏠 Home route
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

# 📝 Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "⚠️ Passwords do not match."

        hashed_password = generate_password_hash(password)

        if users_col.find_one({"email": email}):
            return "⚠️ Email already registered."

        users_col.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })
        return render_template('account_created.html', name=name)
    return render_template('signup.html')

# 🔑 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_col.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            return redirect('/dashboard')
        else:
            return "❌ Invalid email or password."
    return render_template('login.html')

# 🧠 Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']

    saved = passwords_col.find({"user": user})
    passwords = [{"service": s["service"], "password": s["password"]} for s in saved]

    return render_template('dashboard.html', username=user, passwords=passwords)

# 🚪 Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# 💾 Save password route
@app.route('/save_password', methods=['POST'])
def save_password():
    if 'user' not in session:
        return "Unauthorized", 401

    service = request.form['service']
    password = request.form['password']
    user = session['user']

    passwords_col.insert_one({
        "user": user,
        "service": service,
        "password": password
    })
    return '', 200

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)
