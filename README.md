# IoT DHT11 Sensor Project

## Introduction
This project demonstrates how to use the DHT11 sensor to monitor temperature and humidity levels. The data collected by the sensor is processed and displayed using an IoT platform.

## Features
- Real-time temperature and humidity monitoring
- Data visualization on an IoT dashboard
- Easy-to-follow setup instructions
- Robust error handling
- Local database logging
- MQTT data transmission

## Requirements

# Hardware 
- DHT11 sensor
- Raspberry pi 4
- Jumper wires
- Breadboard
- Internet connection (WIFI)

# Prerequisites
- Raspberry Pi with Raspbian OS installed
- Python and pip installed
- MQTT broker credentials


# Software
- Python 3.7+
- Libraries: 
    - Adafruit_DHT
    - Paho-mqtt
    - sqlite3 

    ![DHT11 Connection Diagram](images/sensor_diagram.png)

## Setup Instructions
# 1.Install required libraries:
```bash
pip install Adafruit_DHT paho-mqtt
```
# 2.Connect the DHT11 sensor to the microcontroller as shown in the diagram:
![Hardware connection](images/rasp_Sensor.png)
# 3.Configure MQTT broker settings in the code
# 4.Create SQLite database:
```sql
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL,
);
```
# 5.Upload the provided code to your Raspberry Pi

## Code Example
```py
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
```

## Visualization
Once the data is being sent to your IoT platform, you can visualize it using graphs and charts:

![IoT Dashboard](images/senasteVersionen_DHT11.png)

## Troubleshooting
- Verify all wire connections
- Check MQTT broker credentials
- Ensure Python libraries are installed
- Confirm sensor compatibility with Raspberry Pi

## Performance Optimization
- Adjust sampling rate as needed
- Implement caching mechanisms
- Use connection pooling for database

## Contributing
# 1.Fork the repository.
# 2.Create a feature branch.
# 3.Commit your changes.
# 4.Push to the branch.
# 5.Create a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
# For questions or support, please open an issue in the GitHub repository.
