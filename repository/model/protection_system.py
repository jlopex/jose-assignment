from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class ProtectionSystem(Base):
    __tablename__ = "protection_system"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    encryption_mode: Mapped[str] = mapped_column(String(64))

