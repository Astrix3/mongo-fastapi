import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from api.endpoints.course import router as course_router

app = FastAPI()

@app.on_event("startup")
async def init_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.db_url)
    app.mongodb = app.mongodb_client[settings.db_name]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(course_router, tags=["Course"], prefix="/course")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
    )
