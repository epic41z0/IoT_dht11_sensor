import time
import adafruit_dht
import board
import sqlite3
import paho.mqtt.client as mqtt

# Inställningar för DHT11-sensorn
dht_device = adafruit_dht.DHT11(board.D4)

# MQTT-inställningar
broker = "localhost"
port = 1883
topic = "sensor/data"
username = "ditt_användarnamn"
password = "nackademin2023"

# Skapa en MQTT-klient
client = mqtt.Client()
client.username_pw_set(username, password)

# Anslut till MQTT-brokern
try:
    client.connect(broker, port)
    print("Ansluten till MQTT-brokern.")
except Exception as e:
    print(f"Kunde inte ansluta till MQTT-brokern: {e}")
    exit(1)

# Anslut till SQLite-databasen
conn = sqlite3.connect('sensordata.db')
cursor = conn.cursor()

# Funktion för att logga data i databasen och skicka till MQTT
def log_data(temperature, humidity):
    # Skicka till MQTT
    payload = f"{{'temperature': {temperature}, 'humidity': {humidity}}}"
    result = client.publish(topic, payload)
    if result.rc == 0:
        print(f"Data skickad till MQTT: {payload}")
    else:
        print(f"Misslyckades med att skicka data till MQTT. Status: {result.rc}")

    # Spara i databasen med felhantering
    try:
        cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
        conn.commit()
        print("Data sparad i databasen")
    except sqlite3.Error as db_error:
        print(f"Fel vid insättning i databasen: {db_error}")

# Huvudloop för att läsa och logga sensordata
try:
    while True:
        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                print(f"Temperatur: {temperature_c:.1f} °C, Luftfuktighet: {humidity}%")
                log_data(temperature_c, humidity)
            else:
                print("Ingen data tillgänglig")

        except RuntimeError as error:
            print(f"Fel vid inläsning: {error}")
            time.sleep(2)

        time.sleep(5)

except KeyboardInterrupt:
    print("Avbryter programmet")

finally:
    dht_device.exit()
    client.disconnect()
    conn.close()
    print("MQTT-klienten och databasen är frånkopplade.")
