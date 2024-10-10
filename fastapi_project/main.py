import os, threading
from fastapi import FastAPI
from dotenv import load_dotenv
from .middleware import LoggingMiddleware
from .database import exploration_production_collection, financial_performance_collection, health_safety_environment_collection
from .models import ExplorationProduction, FinancialPerformance, HealthSafetyEnvironment
from .kafka_producer import send_kafka_message
#from .kafka_consumer import start_consumer
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uvicorn

load_dotenv()

database_url = os.getenv("DATABASE_URL")
jaeger_host = os.getenv("JAEGER_AGENT_HOSTNAME")
jaeger_port = int(os.getenv("JAEGER_AGENT_PORT"))

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name = jaeger_host,
    agent_port = jaeger_port,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
    
app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(LoggingMiddleware)

@app.get("/")
def main_root():
    with tracer.start_as_current_span("main_root"):
        return {"Hello": "World"}

@app.get("/health")
def health_check():
    with tracer.start_as_current_span("health_check"):
        return {"status": "healthy"}

@app.post("/add_exploration_production")
def add_exploration_production(data: ExplorationProduction):
    with tracer.start_as_current_span("add_exploration_production"):
        kpi_data = data.model_dump()
        send_kafka_message('exploration_production', kpi_data)
        return {"status": "Exploration & Production KPI data sent and stored."}
    
@app.post("/add_financial_performance")
def add_financial_performance(data: FinancialPerformance):
    with tracer.start_as_current_span("add_financial_performance"):
        kpi_data = data.model_dump()
        send_kafka_message('financial_performance', kpi_data)
        return {"status": "Financial Performance KPI data sent and stored."}
    
@app.post("/add_health_safety_environment")
def add_health_safety_environment(data: HealthSafetyEnvironment):
    with tracer.start_as_current_span("add_health_safety_environment"):
        kpi_data = data.model_dump()
        send_kafka_message('health_safety_environment', kpi_data)
        return {"status": "Health, Safety, and Environment KPI data sent and stored."}
    
#@app.on_event("startup")
#def startup_event():
#   threading.Thread(target = start_consumer, daemon = True).start()
    
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8080)
