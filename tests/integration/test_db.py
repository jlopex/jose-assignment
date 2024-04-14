# Tests DB integration
from sqlalchemy import text

from src.repository.db import new_session
from tests.integration.common import DBTestBase


class TestDb(DBTestBase):
    def setup_method(self):
        with new_session() as session:
            result = session.execute(text("select 1"))

        assert result.one() == (1,)
