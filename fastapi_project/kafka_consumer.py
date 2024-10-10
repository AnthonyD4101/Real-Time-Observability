import os, json, logging, sys, six

# https://github.com/dpkp/kafka-python/issues/2412
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
from .database import (
    exploration_production_collection,
    financial_performance_collection,
    health_safety_environment_collection,
    exploration_kpi_collection,
    financial_kpi_collection,
    health_kpi_collection
)
from dotenv import load_dotenv

load_dotenv()

# kafka_broker = os.getenv("KAFKA_BROKER")
kafka_broker = 'localhost:9092'

def calculate_exploration_kpi(data):
    """
    Calculate KPIs based on ExplorationProduction data.
    Mock KPI 1: Drilling Success Rate (%)
    Mock KPI 2: Machine Downtime (lower is better)
    Mock KPI 3: Operational Efficiency (%)
    """
    drilling_success_rate = sum(item["drilling_success_rate"] for item in data) / len(data)
    avg_machine_downtime = sum(item["machine_downtime"] for item in data) / len(data)
    avg_operational_efficiency = sum(item["operational_efficiency"] for item in data) / len(data)
    
    return {
        "drilling_success_rate": drilling_success_rate,
        "avg_machine_downtime": avg_machine_downtime,
        "avg_operational_efficiency": avg_operational_efficiency
    }

def calculate_financial_kpi(data):
    """
    Calculate KPIs based on FinancialPerformance data.
    Mock KPI 1: Revenue Growth Rate (simple average)
    Mock KPI 2: Net Income to Revenue Ratio (profit margin)
    """
    total_revenue = sum(item["revenue"] for item in data)
    total_net_income = sum(item["net_income"] for item in data)
    
    avg_revenue_growth_rate = (total_revenue / len(data))
    avg_net_income_ratio = (total_net_income / total_revenue) if total_revenue > 0 else 0
    
    return {
        "avg_revenue_growth_rate": avg_revenue_growth_rate,
        "avg_net_income_ratio": avg_net_income_ratio
    }

def calculate_health_kpi(data):
    """
    Calculate KPIs based on HealthSafetyEnvironment data.
    Mock KPI 1: Lost Time Incident Rate (lower is better)
    Mock KPI 2: Environmental Compliance Rate (%)
    """
    avg_lost_time_incident_rate = sum(item["lost_time_incident_rate"] for item in data) / len(data)
    avg_environmental_compliance_rate = sum(item["environmental_compliance_rate"] for item in data) / len(data)
    
    return {
        "avg_lost_time_incident_rate": avg_lost_time_incident_rate,
        "avg_environmental_compliance_rate": avg_environmental_compliance_rate
    }

def start_consumer():
    logging.info(f"Starting Kafka consumer on broker {kafka_broker}")
    try:
        consumer = KafkaConsumer(
            'health_safety_environment',
            'financial_performance',
            'exploration_production',
            bootstrap_servers = [kafka_broker],
            group_id='kpi_calculator_consumer_group',
            value_deserializer = lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset = 'earliest',
            enable_auto_commit = True,
        )
    
    except Exception as e:
        logging.error(f"Failed to connect to Kafka broker: {e}")
        sys.exit(1)


    for message in consumer:
        logging.info(f"Received message from topic {message.topic}")
        process_message(message)

def process_message(message):
    try:
        topic = message.topic
        data = message.value

        logging.info(f"Processing message from topic {topic}: {data}")

        if topic == 'health_safety_environment':
            health_safety_environment_collection.insert_one(data)
            health_kpi = calculate_health_kpi([data])
            health_kpi_collection.insert_one(health_kpi)
            logging.info(f"Inserted data and KPIs for health_safety_environment")

        elif topic == 'financial_performance':
            financial_performance_collection.insert_one(data)
            financial_kpi = calculate_financial_kpi([data])
            financial_kpi_collection.insert_one(financial_kpi)
            logging.info(f"Inserted data and KPIs for financial_performance")

        elif topic == 'exploration_production':
            exploration_production_collection.insert_one(data)
            exploration_kpi = calculate_exploration_kpi([data])
            exploration_kpi_collection.insert_one(exploration_kpi)
            logging.info(f"Inserted data and KPIs for exploration_production")

    except Exception as e:
        logging.error(f"Error processing message: {e}")

if __name__ == "__main__":
    start_consumer()