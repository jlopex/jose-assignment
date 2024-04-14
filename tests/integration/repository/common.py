from src.repository import db


class DBTestBase:
    def setup_method(self):
        db.init("sqlite:///:memory:", debug=False)
