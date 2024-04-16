from src.common.unicorn_exception import UnicornException
from src.repository.content import ContentRepository
from src.repository.device import DeviceRepository


class SecurityError(UnicornException):
    pass


class SecurityInvalidProtection(SecurityError):
    pass


class SecurityService:
    @staticmethod
    def check_can_decrypt(device_id: int, content_id: int) -> None:
        device = DeviceRepository.get(device_id)
        content = ContentRepository.get(content_id)

        if device.protection_system.id != content.protection_system.id:
            raise SecurityInvalidProtection(
                f"Invalid protection system {device.protection_system.name}"
            )
