from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from .protection_system import ProtectionSystem


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    protection_system_id: Mapped[int] = mapped_column(
        ForeignKey("protection_system.id")
    )
    protection_system: Mapped["ProtectionSystem"] = relationship()
