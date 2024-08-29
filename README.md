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

# Build and run docker deployment:

docker build -t fastapi-app .

docker run -d -p 8080:8080 fastapi-app
