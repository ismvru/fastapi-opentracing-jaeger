#!/usr/bin/env python3
from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
import uvicorn

sampler = TraceIdRatioBased(1 / 1000)
tracer = trace.get_tracer(__name__)
trace_provider = TracerProvider(
    resource=Resource.create({"service.name": "open-telemetry-test"})
)
exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
span_processor = BatchSpanProcessor(exporter)
trace_provider.add_span_processor(span_processor)
app = FastAPI()


@app.get("/")
async def helloworld(request: Request):
    return {"Hello": "World"}


if __name__ == "__main__":

    FastAPIInstrumentor.instrument_app(app=app, tracer_provider=trace_provider)
    uvicorn.run(app, host="0.0.0.0")
