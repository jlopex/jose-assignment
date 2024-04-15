from http import HTTPStatus

from starlette import status
from starlette.responses import JSONResponse

from src.repository.content import ContentRepository
from src.service.crypto import CryptoService
from src.service.security import SecurityService
from ._base import app, BASE_ROUTE
from .responses.content import ContentCreateResponse, ContentResponse
from .schemas.content_create import ContentCreateSchema
from ..domain.content import ContentCreate
from ..repository.protection_system import ProtectionSystemRepository

ROUTE = f"{BASE_ROUTE}/content"


@app.get("/api/content/{id}", response_model=ContentResponse)
async def get_content(id: int, device_id: int):
    content = ContentRepository.get(id)
    SecurityService.check_can_decrypt(device_id=device_id, content_id=id)
    decoded_payload = CryptoService.decrypt(content=content).encrypted_payload

    return ContentResponse(
        payload=decoded_payload,
        symmetricKey=content.encryption_key,
        protectionSystem=content.protection_system.name,
    )


@app.post(
    "/api/content/",
    status_code=HTTPStatus.CREATED,
    response_model=ContentCreateResponse,
)
async def add_content(new_content: ContentCreateSchema):
    protection_systems = ProtectionSystemRepository.find(
        name=new_content.protectionSystem
    )
    if not protection_systems:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": f"Protection System [{new_content.protectionSystem}] not found"
            },
        )

    # If different protection systems cannot have the same name, consider using UNIQUE constraint.
    protection_system = protection_systems[0]
    crypted_content = CryptoService.encrypt(
        ContentCreate(
            protection_system_id=protection_system.id,
            encryption_key=new_content.symmetricKey,
            encrypted_payload=new_content.payload,
        )
    )
    content = ContentRepository.create(crypted_content)

    return {
        "id": content.id,
        "size": len(crypted_content.encrypted_payload),
    }
