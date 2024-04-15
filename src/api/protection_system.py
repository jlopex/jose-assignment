from http import HTTPStatus

from src.repository.protection_system import ProtectionSystemRepository
from ._base import app, BASE_ROUTE
from .responses.protection_system import ProtectionSystemResponse
from .schemas.protection_system_create import ProtectionSystemCreateSchema

ROUTE = (
    f"{BASE_ROUTE}/protection-systems"  # Unused for the moment (need to create a Route)
)


@app.get("/api/protection-systems/{id}", response_model=ProtectionSystemResponse)
async def get_protection_system(id: int):
    return ProtectionSystemResponse.from_entity(ProtectionSystemRepository.get(id))


@app.get("/api/protection-systems/", response_model=list[ProtectionSystemResponse])
async def list_protection_systems(name: str | None = None):
    filter = {}
    if name:
        filter["name"] = name

    return [
        ProtectionSystemResponse.from_entity(ps)
        for ps in ProtectionSystemRepository.find(**filter)
    ]


@app.post(
    "/api/protection-systems/",
    status_code=HTTPStatus.CREATED,
    response_model=ProtectionSystemResponse,
)
async def create_protection_system(protection_system: ProtectionSystemCreateSchema):
    return ProtectionSystemResponse.from_entity(
        ProtectionSystemRepository.create(protection_system)
    )
