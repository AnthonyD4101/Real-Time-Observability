Simple FastAPI application integrated with MongoDB and Jaeger for distributed tracing and telemetry. It provides a basic API endpoint and demonstrates how to log and trace requests across the application.

# Installing needed dependencies:

python -m pip install --upgrade pip

pip install -r requirements.txt

# Create a .env file to store the following:

DATABASE_URL = mongodb+srv://fastAdmin:admin123!@personalprojects.uuknh.mongodb.net/?retryWrites=true&w=majority&appName=PersonalProjects

JAEGER_AGENT_HOSTNAME = localhost

JAEGER_AGENT_PORT = 5775

# Running tests:

pytest

# JeagerUI Docker Command

docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 -p 5775:5775/udp -p 14250:14250 -p 14268:14268 -p 16686:16686 jaegertracing/all-in-one:1.35

# FastAPI Build Docker Image

docker build -t fastapi-jaeger-collector .

# FastAPI Run Docker Image

docker run -d -p 8080:8080 fastapi-jaeger-collector

# Viewing in localhost

FastAPI UI: http://localhost:8080/docs

Jaeger UI: http://localhost:16686

# Accessing Messages from Kafka Topic

`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic exploration_production --from-beginning`
`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic financial_performance --from-beginning`
`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic health_safety_environment --from-beginning`

# Running Kafka Consumer for Raw Data and KPI Data to be Sent to MongoDB

`python -m fastapi_project.kafka_consumer`
