from pydantic import BaseModel


class ContentCreateSchema(BaseModel):
    protectionSystem: str
    symmetricKey: str
    payload: str
