# Real-Time KPI Dashboard

This project is a KPI Metrics Dashboard designed to visualize key performance indicators (KPIs) across various domains, such as Exploration, Financial, and Health.

It aggregates data from MongoDB and displays real-time metrics in a terminal-based interface (using Python Rich), with color-coded values to indicate performance against predefined thresholds.

The project is useful for monitoring KPIs to ensure compliance with Service Level Agreements (SLAs) and overall operational health.

## Installing Needed Dependencies:

python -m pip install --upgrade pip

pip install -r requirements.txt

## Create a .env file to store the following:

DOCKER_USERNAME={Enter Docker Username Credentials}

DOCKER_PASSWORD={Enter Docker Password Credentials}

DATABASE_URL=mongodb+srv://fastAdmin:admin123@personalprojects.uuknh.mongodb.net/?retryWrites=true&w=majority&appName=PersonalProjects
JAEGER_AGENT_HOSTNAME=jaeger

JAEGER_AGENT_PORT=6831

KAFKA_BROKER=broker:29092

## Run Docker Compose File (FastAPI, Jaeger, MongoDB, Apache Zookeeper and Apache Kafka Setup)

`docker-compose up --build`

## Scripts Needed to Run

After those services are running, you will need to start running scripts to get into the pipeline flow (all these scripts should
be ran in different terminals):

1. Generating Mock Data to hit FastAPI Endpoints (run from fastapi_project directory)

`python data_generator.py`

2. Run Kafka Consumer to Take Data From Kafka Topic and 'Transform' it, to Then Send to MongoDB (run from root directory)

`python -m fastapi_project.kafka_consumer`

3. Generate Real-Time Dashboard to Track Calculated KPIs (run from fastapi_project directory)

`python kpi_text_dashboard.py`

### [Additional Stuff] Accessing Messages from Kafka Topic

`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic exploration_production --from-beginning`

`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic financial_performance --from-beginning`

`kafka-console-consumer.sh --bootstrap-server broker:9092 --topic health_safety_environment --from-beginning`
