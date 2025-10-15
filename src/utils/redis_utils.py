import json
import redis.asyncio as redis
from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage
from typing import List


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
storage = RedisStorage(redis_client)

# https://redis.io/docs/latest/develop/clients/redis-py/ Доки для редиса


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


async def set_media_group_to_forward(messages: List[Message], key: str, expire_seconds: int = 300) -> None:
    # We first dump every single message into a dict type json. Then we dump this message dict (json) into json str
    # Then we add it into a dict as a value, where the key is message's id. That way we get {int: str}
    # Redis hsetex only takes a dict with types int or str
    # Unlike just Redis.hset, hsetex can take expiration time that is crucial for the bot's logic
    serialized = {message.message_id: json.dumps(message.model_dump()) for message in messages}  
    await redis_client.hsetex(key=key, mapping=serialized, ex=expire_seconds)


async def get_media_group_to_forward(key: str) -> List[Message] | None:
    data = await redis_client.hgetall(name=key)
    if not data:
        return None
    message_dicts = json.loads(data)
    # Convert each dict back into aiogram Message objects
    return List(Message.model_validate(d) for d in message_dicts)


async def delete_saved_message(key: str) -> None:
    await redis_client.delete(key)
