from src.repository import db


class DBTestBase:
    def setup_class(self):
        db.init("sqlite:///:memory:")
