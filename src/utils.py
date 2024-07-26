from time import time
from hashlib import md5


def generate_base_deeplink(group_id: int) -> str:
    return md5(f'{group_id}{time()}'.encode("utf-8"), usedforsecurity=False)
