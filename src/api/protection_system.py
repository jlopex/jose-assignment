from http import HTTPStatus

from src.repository.protection_system import ProtectionSystemRepository
from ._base import app, BASE_ROUTE
from .responses.protection_system import ProtectionSystemResponse
from .schemas.protection_system_create import ProtectionSystemCreateSchema

ROUTE = f"{BASE_ROUTE}/protection-system"


@app.get("/api/protection-systems/{id}", response_model=ProtectionSystemResponse)
async def get_protection_system(id: int):
    return ProtectionSystemResponse.from_entity(ProtectionSystemRepository.get(id))


@app.post("/api/protection-systems/", status_code=HTTPStatus.CREATED)
async def create_protection_system(protection_system: ProtectionSystemCreateSchema):
    return ProtectionSystemResponse.from_entity(
        ProtectionSystemRepository.create(protection_system)
    )
