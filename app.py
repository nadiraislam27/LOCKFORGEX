from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret in production

# 🔒 Initialize database and users table
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

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

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "⚠️ Email already registered."
        conn.close()
        return render_template('account_created.html', name=name)
    return render_template('signup.html')

# 🔑 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT name, password FROM users WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[1], password):
            session['user'] = result[0]  # Store name in session
            return redirect('/dashboard')
        else:
            return "❌ Invalid email or password."
    return render_template('login.html')

# 🧠 Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

# 🚪 Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)