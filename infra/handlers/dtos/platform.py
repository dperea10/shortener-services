from pydantic import BaseModel

class PlatformDTO(BaseModel):
    platform_name: str
    is_web: bool