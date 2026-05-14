from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend

# Initialize DB
conn = sqlite3.connect('history.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature TEXT,
        date_time TEXT
    )
''')
conn.commit()

# Save search
@app.route('/save', methods=['POST'])
def save_search():
    data = request.get_json()
    city = data.get('city')
    temp = data.get('temperature')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO searches (city, temperature, date_time) VALUES (?, ?, ?)", (city, temp, now))
    conn.commit()
    return jsonify({"status":"success"})

# Get history
@app.route('/history', methods=['GET'])
def get_history():
    c.execute("SELECT city, temperature, date_time FROM searches ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    history = [{"city": r[0], "temperature": r[1], "time": r[2]} for r in rows]
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
