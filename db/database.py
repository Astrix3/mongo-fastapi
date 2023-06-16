import os

from bson import ObjectId
from dotenv import load_dotenv
from enum import Enum
from fastapi import Request
from typing import List

from utils.serializer import serializeDict, serializeList

load_dotenv()

class Collections(str, Enum):
    COURSE=os.getenv("COURSE_COLLECTION", "courses")
    CHAPTER=os.getenv("CHAPTER_COLLECTION", "chapters")

async def get_all(collection: Collections, request: Request, filter: dict = {}, limit: int = 100) -> List:
    data = await request.app.mongodb[collection].find(filter).to_list(limit)
    return serializeList(data)

async def get_by_id(collection: Collections, id: str, request: Request) -> dict:
    data = await get(collection, request, {"_id": ObjectId(id)})
    return serializeDict(data)

async def get(collection: Collections, request: Request, condition: dict = {}) -> dict:
    data = await request.app.mongodb[collection].find_one(condition)
    return serializeDict(data)

async def insert(collection: Collections, request: Request, data: dict):
    await request.app.mongodb[collection].insert_one(data)

async def update_by_id(collection: Collections, request: Request, data: dict, id):
    await request.app.mongodb[collection].update_one({"_id": ObjectId(id)}, data)