from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.db.database import sessionmanager
from app.routers import book_router, auth_router
from app.settings.config import DATABASE_URL
from app.service.seed_service import load_seed_data
# import asyncio
import app.models
from app.core.exception_handler import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(book_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")
# async def main():
#     sessionmanager.init(DATABASE_URL)
#     await sessionmanager.init_db()
#     await load_seed_data()

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(app, host="127.0.0.1", port=8084, workers=1)


