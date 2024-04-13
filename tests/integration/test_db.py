# Tests DB integration
from sqlalchemy import text

from src.repository.db import new_session


class TestDb:
    def test_select_one(self):
        with new_session() as session:
            result = session.execute(text('select 1'))

        assert result.one() == (1,)
