from src.domain.content import Content, ContentCreate
from src.repository import model
from src.repository.db import generic_create, generic_get, generic_delete
from src.repository.exceptions import RepositoryUnencryptedContentError

__all__ = ("ContentRepository",)


class ContentRepository:
    @staticmethod
    def create(new_content: ContentCreate) -> Content:
        if not new_content.is_encrypted:
            raise RepositoryUnencryptedContentError("Content needs to be encrypted")

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
