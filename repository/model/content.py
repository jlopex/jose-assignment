from sqlalchemy import ForeignKey, String, BLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from .protection_system import ProtectionSystem


class Content(Base):
    __tablename__ = 'content'

    id: Mapped[int] = mapped_column(primary_key=True)
    encryption_key: Mapped[str] = mapped_column(String(128))
    encrypted_payload: Mapped[bytes] = mapped_column(BLOB)
    protection_system_id: Mapped[int] = mapped_column(ForeignKey("protection_system.id"))
    protection_system: Mapped["ProtectionSystem"] = relationship()
