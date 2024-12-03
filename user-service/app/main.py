from fastapi import FastAPI, Request
from app.routes import user_router, admin_router
from app.db import Base, engine
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="A microservice to manage E-commerce Users.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Initialize
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admins"])

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Use Render's Jaeger URL or your Jaeger service
    agent_port=6831,
)

resource = Resource(attributes={
    SERVICE_NAME: "user-service"
})

# Instrumentation
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(trace_provider)
otlp_exporter = OTLPSpanExporter(endpoint="http://collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace_provider)
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the User Service!"}

@app.get("/login")
@limiter.limit("5/minute")
async def login(request: Request):
    return {"message": "Login endpoint"}

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002)