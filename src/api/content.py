from http import HTTPStatus
from io import BytesIO

from fastapi import UploadFile
from starlette.responses import StreamingResponse

from src.domain.content import ContentCreate
from src.repository.content import ContentRepository
from src.service.crypto import CryptoService
from src.service.security import SecurityService
from ._base import app, BASE_ROUTE
from .responses.content import ContentCreateResponse
from .responses.device import DeviceResponse

ROUTE = f"{BASE_ROUTE}/content"


@app.get("/api/content/{id}", response_model=DeviceResponse)
async def get_content(id: int, device_id: int):
    content = ContentRepository.get(id)
    SecurityService.check_can_decrypt(device_id=device_id, content_id=id)
    decoded_payload = CryptoService.decrypt(content=content).encrypted_payload

    headers = {"Content-Disposition": 'attachment; filename="blob.bin"'}
    output = BytesIO(decoded_payload)
    return StreamingResponse(output, headers=headers)


@app.post(
    "/api/content/{protection_system_id}/upload/{key}",
    status_code=HTTPStatus.CREATED,
    response_model=ContentCreateResponse,
)
async def add_content(protection_system_id: int, key: str, file: UploadFile):
    file_content = await file.read()
    new_content = ContentCreate(
        protection_system_id=protection_system_id,
        encryption_key=key,
        encrypted_payload=file_content,
    )

    crypted_content = CryptoService.encrypt(new_content)
    content = ContentRepository.create(crypted_content)

    return {
        "id": content.id,
        "filename": file.filename,
        "size": len(file_content),
    }
