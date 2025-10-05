import json
import redis.asyncio as redis
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage
from typing import List


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
storage = RedisStorage(redis_client)


async def set_message_to_forward(
    redis_client: 
    redis.Redis, 
    message: Message, 
    key: str, 
    expire_seconds: int = 300
) -> None:
    message_dict = message.model_dump()  # Convert Message object to dict (aiogram v3)
    message_json = json.dumps(message_dict)
    await redis_client.set(key, message_json, ex=expire_seconds)


async def get_message_to_forward(redis_client: redis.Redis, key: str) ->  Message | None:
    message_json = await redis_client.get(key)
    if message_json:
        message_dict = json.loads(message_json)
        return Message(**message_dict)
    return None


async def set_media_group_to_forward(
    redis_client: 
    redis.Redis, 
    messages: List[Message], 
    key: str, 
    expire_seconds: int = 300
) -> None:
    ...
