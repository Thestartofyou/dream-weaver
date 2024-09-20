# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup: SQLite for simplicity
def init_db():
    conn = sqlite3.connect('dreams.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dreams 
                (id INTEGER PRIMARY KEY, username TEXT, title TEXT, dream_story TEXT)''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    conn = sqlite3.connect('dreams.db')
    c = conn.cursor()
    c.execute("SELECT * FROM dreams")
    dreams = c.fetchall()
    conn.close()
    return render_template('home.html', dreams=dreams)

# Route to submit new dream
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        dream_story = request.form['dream_story']
        
        conn = sqlite3.connect('dreams.db')
        c = conn.cursor()
        c.execute("INSERT INTO dreams (username, title, dream_story) VALUES (?, ?, ?)",
                  (username, title, dream_story))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    
    return render_template('submit.html')

# Route to view a specific dream
@app.route('/dream/<int:dream_id>')
def view_dream(dream_id):
    conn = sqlite3.connect('dreams.db')
    c = conn.cursor()
    c.execute("SELECT * FROM dreams WHERE id=?", (dream_id,))
    dream = c.fetchone()
    conn.close()
    return render_template('view_dream.html', dream=dream)

# Initialize the database
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
