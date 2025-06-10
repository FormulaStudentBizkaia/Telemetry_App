import redis

class redisConector:
    def __init__(self) -> None:
        # connect to redis
        self.client = redis.Redis(host='redis', port=6379, health_check_interval=30, decode_responses=True)

    def get_value(self, id) -> str:
        return self.client.get(id)