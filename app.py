from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "84251379358517826681762094589523"  # Your secret key

# MongoDB Atlas connection
MONGODB_URI = "mongodb+srv://lockforgex:22334455@lockforgex.v4uoa2q.mongodb.net/lockforgex"
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

# 📝 Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "⚠️ Passwords do not match."

        if users_col.find_one({"email": email}):
            return "⚠️ Email already registered."

        hashed_password = generate_password_hash(password)
        users_col.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })
        return render_template('account_created.html', name=name)
    return render_template('signup.html')

# 🔑 Login
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

# 🧠 Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    saved_passwords = passwords_col.find({"user": user})
    passwords = [{"service": p["service"], "password": p["password"]} for p in saved_passwords]
    return render_template('dashboard.html', username=user, passwords=passwords)

# 💾 Save password
@app.route('/save_password', methods=['POST'])
def save_password():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    service = request.form['service']
    password = request.form['password']
    user = session['user']

    passwords_col.insert_one({
        "user": user,
        "service": service,
        "password": password
    })
    return jsonify({"message": "Password saved!"}), 200

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# 🔎 Optional: test route to view all saved passwords (for debugging)
@app.route('/all_passwords')
def all_passwords():
    all_data = list(passwords_col.find({}, {"_id": 0}))
    return jsonify(all_data)

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)
