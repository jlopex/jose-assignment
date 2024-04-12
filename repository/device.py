from sqlalchemy.orm import Session

from schemas.new_device import NewDeviceSchema
from repository import model
from domain.device import Device


def create(db: Session, new_device: NewDeviceSchema) -> Device:
    db_device = model.Device(name=new_device.name, protection_system_id=new_device.protection_system_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return Device.from_orm(db_device)
