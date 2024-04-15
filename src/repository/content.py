from src.domain.content import Content, ContentCreate
from src.repository import model
from src.repository.db import (
    generic_create,
    generic_get,
    generic_delete,
    generic_update,
)
from src.repository.exceptions import RepositoryUnencryptedContentError

__all__ = ("ContentRepository",)


class ContentRepository:
    @staticmethod
    def _check_is_encrypted(content: Content | ContentCreate):
        if not content.is_encrypted:
            raise RepositoryUnencryptedContentError("Content needs to be encrypted")

    @staticmethod
    def create(new_content: ContentCreate) -> Content:
        ContentRepository._check_is_encrypted(new_content)

        db_device = model.Content(**new_content.model_dump(exclude={"is_encrypted"}))
        content = generic_create(db_device, Content)
        return Content(
            **content.model_dump(exclude={"is_encrypted"}), is_encrypted=True
        )

    @staticmethod
    def get(id: int) -> Content:
        content = generic_get(id, model.Content, Content)
        return Content(
            **content.model_dump(exclude={"is_encrypted"}), is_encrypted=True
        )

    @staticmethod
    def delete(id: int):
        generic_delete(model.Content, id=id)

    @staticmethod
    def update(updated_content: Content) -> Content:
        ContentRepository._check_is_encrypted(updated_content)
        generic_update(
            updated_content.id,
            model.Content,
            protection_system_id=updated_content.protection_system.id,
            **updated_content.model_dump(
                exclude={"id", "is_encrypted", "protection_system"}
            )
        )
