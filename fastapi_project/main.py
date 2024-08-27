from fastapi import FastAPI
from .middleware import LoggingMiddleware
from .database import collection
from .models import UserInfo
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uvicorn

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name = 'localhost',
    agent_port = 5775,
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

@app.post("/addUser")
def create_user(user_info: UserInfo):
    with tracer.start_as_current_span("create_user"):
        user_dict = user_info.model_dump()
        result = collection.insert_one(user_dict)
        return {"userID from account creation": str(result.inserted_id)}
    
if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8080)
