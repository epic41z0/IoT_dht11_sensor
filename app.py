from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Funktion för att hämta de senaste sensordata från databasen
def get_latest_data(limit=10):
    conn = sqlite3.connect('sensordata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, temperature, humidity FROM sensor_data ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_latest_data()
    return render_template('index.html', data=data)

# Ny route för att returnera JSON-data
@app.route('/data')
def data():
    rows = get_latest_data(20)  # Hämta de senaste 20 avläsningarna
    data = {
        "timestamps": [row[1] for row in rows][::-1],  # Timestamp är andra kolumnen
        "temperatures": [row[2] for row in rows][::-1],  # Temperatur är tredje kolumnen
        "humidities": [row[3] for row in rows][::-1]     # Luftfuktighet är fjärde kolumnen
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
