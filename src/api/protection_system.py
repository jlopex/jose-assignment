from src.repository.protection_system import ProtectionSystemRepository
from ._base import app, BASE_ROUTE
from .responses.protection_system import ProtectionSystemResponse

ROUTE = f"{BASE_ROUTE}/protection-system"


@app.get("/api/protection-system/{id}", response_model=ProtectionSystemResponse)
async def get_protection_system(id: int):
    return ProtectionSystemResponse.from_entity(ProtectionSystemRepository.get(id))
