from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator
from opentelemetry.trace.status import StatusCode
from sona.core.messages import State
from sona.core.messages.context import Context
from sona.settings import settings

from .base import MiddlewareBase

SERVICE_NAME = settings.SONA_MIDDLEWARE_TRACER_SERVICE_NAME
AGENT_HOST = settings.SONA_MIDDLEWARE_TRACER_JAEGER_HOST
AGENT_PORT = settings.SONA_MIDDLEWARE_TRACER_JAEGER_PORT


class OpenTelemetryTracer(MiddlewareBase):
    def __init__(self, service_name=SERVICE_NAME, host=AGENT_HOST, port=AGENT_PORT):
        self.resource = Resource.create(attributes={"service.name": service_name})
        self.exporter = JaegerExporter(agent_host_name=host, agent_port=port)
        self.provider = TracerProvider(resource=self.resource)
        self.processor = BatchSpanProcessor(self.exporter)
        self.provider.add_span_processor(self.processor)
        trace.set_tracer_provider(self.provider)
        self.tracer = trace.get_tracer("sona.inferencer")

    def wrapper_func(self, ctx: Context, on_context):
        trace_ctx = None
        traceparent = ctx.headers.get("trace")
        if traceparent:
            carrier = {"traceparent": traceparent}
            trace_ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
        with self.tracer.start_as_current_span("inferencer", context=trace_ctx) as span:
            next_ctx: Context = on_context(ctx)
            state: State = next_ctx.current_state
            span.set_attributes(
                {
                    "inferencer.ctx_id": str(next_ctx.id),
                    "inferencer.start_time": next_ctx.start_time,
                    "inferencer.job": state.job_name,
                    "inferencer.node_name": state.node_name,
                    "inferencer.timestamp": state.timestamp,
                    "inferencer.exec_time": state.exec_time,
                }
            )
            span.set_status(StatusCode.ERROR if next_ctx.is_failed else StatusCode.OK)
            return next_ctx
