import redis

class RedisService:
    """Service for managing Redis database operations.

    Handles storage and retrieval of document text in a Redis database.
    Establishes a single Redis client connection with decode_responses enabled.

    Attributes:
        client (redis.Redis): Redis client instance for database operations.
    """
    def __init__(self):
        """Initialize RedisService with a Redis client connection.

        Sets up a connection to the Redis server at host 'redis' and port 6379,
        with decode_responses=True to return strings instead of bytes.
        """
        self.client = redis.Redis(host="redis", port=6379, decode_responses=True)

    def store_document(self, filename: str, text: str):
        """Store document text in Redis.

        Saves the text content associated with a filename as a key-value pair
        in the Redis database.

        Args:
            filename (str): Name of the document to store as the key.
            text (str): Text content to store as the value.
        """
        self.client.set(filename, text)

    def get_document(self, filename: str) -> str:
        """Retrieve document text from Redis.

        Fetches the text content associated with a filename from the Redis database.

        Args:
            filename (str): Name of the document to retrieve.

        Returns:
            str: Retrieved text content, or empty string if not found.
        """
        return self.client.get(filename) or ""
