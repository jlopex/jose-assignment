from http import HTTPStatus

from src.repository.device import DeviceRepository
from ._base import app, BASE_ROUTE
from .responses.device import DeviceResponse
from .schemas.device_create import DeviceCreateSchema

ROUTE = f"{BASE_ROUTE}/devices"


@app.get("/api/devices/{id}", response_model=DeviceResponse)
async def get_device_system(id: int):
    return DeviceResponse.from_entity(DeviceRepository.get(id))


@app.get("/api/devices/", response_model=list[DeviceResponse])
async def list_device_systems(name: str | None = None):
    filter = {}
    if name:
        filter["name"] = name

    return [DeviceResponse.from_entity(d) for d in DeviceRepository.find(**filter)]


@app.post(
    "/api/devices/", status_code=HTTPStatus.CREATED, response_model=DeviceResponse
)
async def create_device_system(device: DeviceCreateSchema):
    return DeviceResponse.from_entity(DeviceRepository.create(device))


@app.delete(
    "/api/devices/{id}",
    status_code=HTTPStatus.ACCEPTED,
)
async def delete_device(id: int):
    DeviceRepository.delete(id)
    return {}
