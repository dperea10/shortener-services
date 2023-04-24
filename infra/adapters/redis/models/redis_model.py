from datetime import datetime

class DataShortenedUrlRedis:
    def __init__(self, long_url: str, short_url:str, hash_url:str, created_at: datetime):
        self.long_url = long_url
        self.short_url = short_url
        self.hash_url = hash_url
        self.created_at = created_at

    def to_dict(self):
        return {
            'short_url': self.short_url,
            'long_url': self.long_url,
            'hash_url': self.hash_url,
            'created_at': self.created_at.isoformat()
        }