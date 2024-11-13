import requests
import time
import random
from datetime import datetime

# FastAPI URL (replace with your actual server URL)
BASE_URL = "http://localhost:8000"

# 1. Create a new sensor
def create_sensor(sensor_type: str, description: str, location: str):
    url = f"{BASE_URL}/sensors"
    sensor_data = {
        "sensor_type": sensor_type,
        "description": description,
        "location": location
    }
    
    try:
        response = requests.post(url, json=sensor_data)
        response.raise_for_status()  # Raise error if HTTP request failed
        sensor_id = response.json()["sensor_id"]
        print(f"Sensor created successfully with ID: {sensor_id}")
        return sensor_id
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

# 2. Send sensor data to the server every 30 seconds
def send_sensor_data(sensor_id: int):
    url = f"{BASE_URL}/sensor_data/{sensor_id}"
    while True:
        # Generate random sensor data (e.g., temperature between 20 and 30 degrees Celsius)
        sensor_value = round(random.uniform(20.0, 30.0), 2)
        timestamp = datetime.utcnow().isoformat()

        # Prepare the payload for a single sensor data point
        sensor_data = {
            "value": sensor_value,
            "timestamp": timestamp
        }

        try:
            response = requests.post(url, json=sensor_data)
            response.raise_for_status()  # Raise error if HTTP request failed
            print(f"Data sent successfully: {sensor_data}")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

        # Wait for 3 seconds before sending the next data point
        #time.sleep(1)

if __name__ == "__main__":
    # Define the sensor details
    sensor_type = "Temperature"
    description = "Outdoor temperature sensor"
    location = "Garden"

    # Step 1: Create a sensor and get its ID
    sensor_id = create_sensor(sensor_type, description, location)
    
    if sensor_id:
        # Step 2: Start sending sensor data every 30 seconds
        send_sensor_data(sensor_id)