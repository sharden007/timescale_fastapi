import asyncio
from confluent_kafka import Producer
import random
from datetime import datetime
import json

# Kafka producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
}

# Create Kafka Producer
producer = Producer(producer_conf)

# Kafka topic to produce sensor data to
topic = 'sensor_data'

# Function to send sensor data to Kafka
def send_sensor_data(sensor_id):
    sensor_value = round(random.uniform(20.0, 30.0), 2)  # Simulate temperature values
    timestamp = datetime.utcnow().isoformat()

    sensor_data = {
        "sensor_id": sensor_id,
        "value": sensor_value,
        "timestamp": timestamp
    }

    # Send data to Kafka topic
    producer.produce(topic, key=str(sensor_id), value=json.dumps(sensor_data))
    producer.flush()
    print(f"Sent data to Kafka: {sensor_data}")

# Simulate sending data every 30 seconds
async def produce_sensor_data(sensor_id):
    while True:
        send_sensor_data(sensor_id)
        await asyncio.sleep(3)  # Produce data every 3 seconds

if __name__ == "__main__":
    sensor_id = 1  # Replace with actual sensor ID
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce_sensor_data(sensor_id))