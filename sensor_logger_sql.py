import sqlite3
import time
from datetime import datetime

# Simulated sensor class (replace with your actual sensor library)
class Sensor:
    def read_acceleration(self):
        return {"x": 0.01, "y": 0.02, "z": 9.81}  # Simulated accel data

    def read_gyroscope(self):
        return {"x": 0.1, "y": 0.2, "z": 0.3}  # Simulated gyro data

# Initialize the sensor
sensor = Sensor()

# SQLite database file
db_file = "sensor_data.db"

# Function to create the database table
def setup_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            accel_x REAL NOT NULL,
            accel_y REAL NOT NULL,
            accel_z REAL NOT NULL,
            gyro_x REAL NOT NULL,
            gyro_y REAL NOT NULL,
            gyro_z REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to log sensor data into the database
def log_sensor_data():
    setup_database()
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        print("Logging sensor data... Press Ctrl+C to stop.")
        while True:
            # Read sensor data
            accel = sensor.read_acceleration()
            gyro = sensor.read_gyroscope()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert data into the database
            cursor.execute("""
                INSERT INTO sensor_data (timestamp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, accel["x"], accel["y"], accel["z"], gyro["x"], gyro["y"], gyro["z"]))
            
            conn.commit()
            
            # Display logged data in the console
            print(f"{timestamp} - Accel: {accel}, Gyro: {gyro}")
            time.sleep(1)  # Delay for 1 second
    except KeyboardInterrupt:
        print("\nData logging stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Run the data logger
if __name__ == "__main__":
    log_sensor_data()
