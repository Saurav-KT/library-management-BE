import time

from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

class Metrics:
    def __init__(self):
        self.request_counter = None
        self.request_duration = None
        self.initialized = False

    def setup_metrics(self):
        """Initialize OpenTelemetry metrics provider and instruments."""
        if self.initialized:
            return

        resource = Resource.create({
            "service.name": "library-management-service",
        })

        reader = PrometheusMetricReader()
        provider = MeterProvider(
            resource=resource,
            metric_readers=[reader],
        )

        metrics.set_meter_provider(provider)
        meter = metrics.get_meter("library.metrics")

        self.request_counter = meter.create_counter(
            name="http_requests_total",
            description="Total HTTP requests",
        )

        self.request_duration = meter.create_histogram(
            name="http_request_duration_ms",
            description="HTTP request duration",
            unit="ms",
        )

        self.initialized = True




    # ---------------------------
    # 3. Middleware
    # ---------------------------
    async def metrics_middleware(self, request, call_next):
        if not self.initialized:
            self.setup_metrics()

        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        attrs = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        }

        self.request_counter.add(1, attributes=attrs)
        self.request_duration.record(duration, attributes=attrs)
        return response

# Singleton instance used by app
metrics_manager = Metrics()