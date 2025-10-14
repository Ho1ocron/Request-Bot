import json
import redis.asyncio as redis
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage
from typing import List


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
storage = RedisStorage(redis_client)


async def set_message_to_forward(
    message: Message, 
    key: str, 
    expire_seconds: int = 300
) -> None:
    message_dict = message.model_dump()  # Convert Message object to dict (aiogram v3)
    message_json = json.dumps(message_dict)
    await redis_client.set(key, message_json, ex=expire_seconds)


async def get_message_to_forward(key: str) ->  Message | None:
    message_json = await redis_client.get(key)
    if message_json:
        message_dict = json.loads(message_json)
        return Message(**message_dict)
    return None


async def set_media_group_to_forward(
    messages: List[Message], 
    key: str, 
    expire_seconds: int = 300
) -> None:
    serialized = [message.model_dump_json() for message in messages]
    await redis_client.rpush(key, *serialized)
    await redis_client.expire(key, expire_seconds)


async def get_media_group_to_forward(key: str) -> List[Message] | None:
    messages_json = await redis_client.lrange(key, 0, -1)
    if not messages_json:
        return None
    messages = [Message.model_validate_json(m) for m in messages_json]
    return messages


async def delete_saved_message(key: str) -> str:
    await redis_client.delete(key)
    return "Your message order is cleared."
