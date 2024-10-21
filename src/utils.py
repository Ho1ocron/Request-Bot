from time import time
from hashlib import md5


def generate_base_deeplink(content: int) -> str:
    return md5(f'{content}'.encode("utf-8"), usedforsecurity=False)
