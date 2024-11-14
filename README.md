# Timescale API (fastAPI)


Creates a high-performance API for streaming, storing, and querying sensor data using FastAPI and TimescaleDB for efficient time-series data storage.


Database: 
Uses Neon serverless Postgres: (account needed)

https://console.neon.tech

Setting up your Database
In this section, you will set up the TimescaleDB extension using Neon's console, add the database's schema, and create the database connection pool and lifecycle management logic in FastAPI. Optionally, you can also add some mock data to test your API endpoints.

Given TimescaleDB is an extension on top of vanilla Postgres, you must first add the extension by running the following SQL in the SQL Editor tab of the Neon console.

CREATE EXTENSION IF NOT EXISTS timescaledb;


To run the application, use uvicorn CLI with the following command in the "src" directory:

uvicorn main:app --host 0.0.0.0 --port 8080
Once the server is running, you can access the API documentation and test the endpoints directly in your browser:

Interactive API Docs (Swagger UI):
Visit http://localhost:8000/docs to access the automatically generated API documentation where you can test the endpoints.
Alternative Docs (ReDoc):
Visit http://localhost:8000/redoc for another style of API documentation.


# Testing the API
You can test your application using HTTPie, a command-line tool for making HTTP requests. The following steps will guide you through creating sensors, streaming data, and querying sensor statistics.

Retrieve sensor statistics for pre-generated data (optional).

If you followed the optional data generation steps, you can retrieve daily statistics for the pre-generated sensors:

http://localhost:8000/daily_avg/1
http://localhost:8000/daily_avg/2

These commands will return the daily statistics (average, min, max, median, and IQR) for the pre-generated temperature and humidity sensors over the last 7 days.

# Create a new sensor.

Start by creating a new sensor (e.g., a temperature sensor for the living room):

http://localhost:8000/sensors sensor_type="temperature" description="Living room temperature sensor" location="Living Room"
You should see a response confirming the creation of the sensor with a unique ID:

{
  "sensor_id": 3,
  "message": "Sensor created successfully."
}
Stream a single sensor data point.

Stream a single data point for the newly created sensor (sensor_id = 3):

http POST http://localhost:8000/sensor_data/3 value:=23.5 timestamp="2024-10-12T14:29:00"
You should get a response indicating success:

{
  "message": "Sensor data streamed successfully."
}
Stream a batch of sensor data.

You can also stream multiple sensor data points in a batch for the same sensor:

http POST http://localhost:8000/sensor_data/3 data:='[{"value": 22.5, "timestamp": "2024-10-12T14:30:00"}, {"value": 22.7, "timestamp": "2024-10-12T14:31:00"}]'
This will send two data points to the sensor. The response will confirm successful streaming of the batch data:

{
  "message": "Sensor data streamed successfully."
}
Retrieve daily statistics for the new sensor.

After streaming the sensor data, you can retrieve the daily statistics for the new sensor (sensor_id = 3):

http GET http://localhost:8000/daily_avg/3
This will return daily statistics (average, min, max, median, and IQR) for the new sensor over the last 7 days:

[
  {
    "day": "2024-10-12",
    "sensor_id": 3,
    "avg_value": 22.6,
    "min_value": 22.5,
    "max_value": 22.7,
    "reading_count": 2,
    "median_value": 22.6,
    "iqr_value": 0.2
  }
]
By following these steps, you can easily create sensors, stream sensor data, and query statistics from your API. For sensors with pre-generated data, you can retrieve the statistics immediately. For new sensors, you can stream data and retrieve their daily stats dynamically.



KAFKA:

After making changes ot kafka-run-class.bat file (if error input line too long) 
run in Powershell Terminal: $ .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties   - to start zookeeper

Then in another powershell Terminal: (start Kafka)


# After making these changes:
- Run your producer (python kafka_producer.py) to generate sensor data.
Run your consumer (python kafka_consumer.py) and monitor for any errors.

Check your PostgreSQL database to ensure that records are being inserted correctly with proper timestamps.

SELECT * FROM public.sensor_data

