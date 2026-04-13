from fastapi import FastAPI, APIRouter
from prometheus_client import generate_latest
from starlette.responses import Response


router = APIRouter(
    prefix="/observability",
    tags=["observability"]
)

@router.get("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), media_type="text/plain")