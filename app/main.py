from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.db.database import sessionmanager
from app.routers import book_router, auth_router, category_router,publisher_router,author_router, member_router, metrices_router
from app.settings.config import DATABASE_URL
from app.service.seed_service import load_seed_data
import app.models
from app.core.exception_handler import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.observability.otel import setup_tracing
from app.observability.metrics import metrics_manager

setup_tracing()

# Initialize once at startup
metrics_manager.setup_metrics()

description = """
Library management APIs
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(DATABASE_URL)
    await sessionmanager.init_db()
    await load_seed_data()
    yield


app = FastAPI(lifespan=lifespan)


register_exception_handlers(app)
app.include_router(book_router.router, prefix="/api")
app.include_router(category_router.router, prefix="/api")
app.include_router(publisher_router.router, prefix="/api")
app.include_router(author_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")
app.include_router(member_router.router, prefix="/api")
app.include_router(metrices_router.router, prefix="/api")

FastAPIInstrumentor.instrument_app(app)
app.middleware("http")(metrics_manager.metrics_middleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# async def main():
#     sessionmanager.init(DATABASE_URL)
#     await sessionmanager.init_db()
#     await load_seed_data()

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(app, host="127.0.0.1", port=8084, workers=1)


