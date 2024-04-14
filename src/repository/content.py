from src.domain.content import Content, ContentCreate
from src.repository import model
from src.repository.db import generic_create, generic_get

__all__ = ("ContentRepository",)


class ContentRepository:
    @staticmethod
    def create(new_content: ContentCreate) -> Content:
        db_device = model.Content(**new_content.model_dump(exclude={"is_encrypted"}))
        return generic_create(db_device, Content)

    @staticmethod
    def get(id: int) -> Content:
        return generic_get(id, model.Content, Content)
