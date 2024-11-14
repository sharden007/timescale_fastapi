import asyncio
from confluent_kafka import Consumer, KafkaException
import asyncpg
import json
from datetime import datetime
from loguru import logger

# NeonDB connection string (PostgreSQL connection)
#DATABASE_URL = "postgres://neondb_owner:PRLt5S7OrKIb@ep-young-grass-a49pw2ze.us-east-1.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL =  "postgres://postgres:Stealth6@localhost/sensor_db"

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker
    'group.id': 'sensor_group',             # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start consuming from the earliest offset
}

# Create Kafka Consumer
consumer = Consumer(conf)

# Subscribe to the 'sensor_data' topic
consumer.subscribe(['sensor_data'])

# Initialize the connection pool globally to reuse connections
conn_pool = None

# Initialize the PostgreSQL connection pool
async def init_db():
    global conn_pool
    try:
        conn_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        logger.info("Database connection pool initialized.")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise

# Function to insert sensor data into NeonDB using the connection pool
async def insert_sensor_data(sensor_id, value, timestamp):
    try:
        async with conn_pool.acquire() as conn:
            # Convert timestamp from string to datetime object
            timestamp_dt = datetime.fromisoformat(timestamp)  # Convert ISO 8601 string to datetime object
            
            # SQL query to insert sensor data into the database
            insert_query = """
            INSERT INTO sensor_data (sensor_id, value, time)
            VALUES ($1, $2, $3);
            """
            await conn.execute(insert_query, sensor_id, value, timestamp_dt)
            logger.info(f"Inserted data into NeonDB: sensor_id={sensor_id}, value={value}, timestamp={timestamp_dt}")
    except Exception as e:
        logger.error(f"Error inserting data into NeonDB: {e}")

# Kafka consumer loop that processes messages and inserts them into NeonDB
async def consume_sensor_data():
    while True:
        msg = consumer.poll(1.0)  # Poll Kafka topic every second
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Kafka error: {msg.error()}")
            continue  # Log the error and continue
        
        try:
            # Decode and parse Kafka message
            sensor_data = json.loads(msg.value().decode('utf-8'))
            sensor_id = sensor_data['sensor_id']
            value = sensor_data['value']
            timestamp = sensor_data['timestamp']

            # Insert the consumed data into NeonDB
            await insert_sensor_data(sensor_id, value, timestamp)

            # Commit Kafka offset after successful insertion
            consumer.commit()

        except Exception as e:
            logger.error(f"Failed to process message: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # Initialize the database connection pool
    loop.run_until_complete(init_db())
    # Start consuming data from Kafka
    loop.run_until_complete(consume_sensor_data())