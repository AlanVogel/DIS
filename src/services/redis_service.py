import redis

class RedisService:
    def __init__(self):
        self.client = redis.Redis(host="redis", port=6379, decode_responses=True)

    def store_document(self, filename: str, text: str):
        self.client.set(filename, text)

    def get_document(self, filename: str) -> str:
        return self.client.get(filename) or ""
