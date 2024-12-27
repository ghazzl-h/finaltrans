import psycopg2
import serial
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Replace with your database connection credentials
database_connection_session = psycopg2.connect(
    host="ep-silent-sound-a5udo5gz.us-east-2.aws.neon.tech",
    database="FinalTrans",
    user="FinalTrans_owner",
    password="efmUkJg41rxS",
    port=5432
)

# Arduino Serial Connection
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

# Global variable to store sensor data
sensor_data = {
    'Distance': "N/A",
    'Motion': "N/A",
    'Temperature': "N/A"
}

# Thread to read data from Arduino
def read_arduino_data():
    global sensor_data
    while True:
        try:
            line = arduino.readline().decode('utf-8').strip()
            if line:
                print(f"Raw Arduino Data: {line}")  # Debug: Log raw Arduino data
                parts = line.split(',')
                for part in parts:
                    key, value = part.split(':')
                    if key.strip() == "Motion":
                        sensor_data[key.strip()] = int(value)
                    else:
                        sensor_data[key.strip()] = float(value)
                print(f"Updated Sensor Data: {sensor_data}")  # Debug: Log updated data
        except Exception as e:
            print(f"Error reading Arduino data: {e}")

# Start the thread to read data
Thread(target=read_arduino_data, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('request_sensor_data')
def send_sensor_data():
    print(f"Sending Sensor Data: {sensor_data}")  # Debug: Log data being sent
    emit('sensor_data', sensor_data)


if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    socketio.run(app, allow_unsafe_werkzeug=True)
