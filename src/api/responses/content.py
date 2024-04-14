from pydantic import BaseModel


class ContentCreateResponse(BaseModel):
    id: int
    filename: str
    size: int
