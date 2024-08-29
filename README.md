Simple FastAPI application integrated with MongoDB and Jaeger for distributed tracing and telemetry. It provides a basic API endpoint and demonstrates how to log and trace requests across the application.

# Installing needed dependencies:

python -m pip install --upgrade pip

pip install -r requirements.txt

# Create a .env file to store the following:

DATABASE_URL = mongodb+srv://fastAdmin:password123!@personalprojects.uuknh.mongodb.net/?retryWrites=true&w=majority&appName=PersonalProjects

JAEGER_AGENT_HOSTNAME = localhost

JAEGER_AGENT_PORT = 5775

# Run the application:

uvicorn fastapi_project.main:app --host 0.0.0.0 --port 8080

# Running tests:

pytest

# JeagerUI Docker Command

docker run -d --name jaeger \
 -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
 -e JAEGER_AGENT_PORT=5775 \
 -e JAEGER_AGENT_HOST=127.0.0.1 \
 -e JAEGER_SERVICE_NAME=my-service \
 -p 5775:5775 \
 -p 14250:14250 \
 -p 14268:14268 \
 -p 16686:16686 \  
 jaegertracing/all-in-one:1.35

# Build Docker Image

docker build -t fastapi-jaeger-collector .

# Run Docker Image

docker run -d -p 8080:8080 fastapi-jaeger-collector

# Viewing in localhost

FastAPI UI: http://localhost:8080/docs

Jaeger UI: http://localhost:16686
