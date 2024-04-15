from pydantic import BaseModel


class ContentCreateResponse(BaseModel):
    id: int
    size: int
    message: str = "encrypted"


class ContentResponse(BaseModel):
    protectionSystem: str
    symmetricKey: str
    payload: str
