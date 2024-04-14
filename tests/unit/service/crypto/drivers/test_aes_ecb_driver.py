from unittest import mock

from src.service.crypto.drivers.aes_ecb import AesEcbDriver


@mock.patch.object(AesEcbDriver, "global_key", return_value=b"dummy-secret")
class TestAesEcbDriver:
    PLAIN_BLOB = """¿Cómo podría yo introducir nuevos dioses por decir que una voz divina se me manifiesta para 
    indicarme lo que hay que hacer?""".encode(
        "utf-8"
    )

    CRYPTED_BLOB: bytes = (
        b"\xbb\xb2\xd7\xfc\xed%\x10\x9b\x0e,\xb9\xeb@\x0e\xd9\x0f\x9a\xd7D-\xb9\x9dL\x80)\xf7\x1f|\t\x0b\r\xd1\x0b|q"
        b"\xa6\xb0\xbe\xfdmxw\x88\x14\xbf+\xbb3\xb3HJ["
        b"\xa3u\xc1\xba#J\x94<\xbd\xc1\x01%\xefIa\xa0\x99Sg\x15\nw\x96\xe6\xe7\x0e?\xa3~\xa9\xf1\x93\xf5\xa8n\xdaU"
        b"\xd0\xefH2}\x87A&CyZ\xc4&\xf2\xc0\xf7A!k\x1b\xee\xcd\xfc\xf1\xe4\xd5\xb5\xa5\t/\xcbF\xd9\xa6\\\xe4{"
        b"\x01\xf1\xa1f\x93"
    )

    def test_crypt(self, m_key):
        crypted_text = AesEcbDriver.encrypt(self.PLAIN_BLOB, key="fake key")
        assert crypted_text == self.CRYPTED_BLOB

    def test_decrypt(self, m_key):
        plain_text = AesEcbDriver.decrypt(self.CRYPTED_BLOB, key="fake key")
        assert plain_text == self.PLAIN_BLOB

    def test_decrypt_with_invalid_key(self, m_key):
        plain_text = AesEcbDriver.decrypt(self.CRYPTED_BLOB, key="fake_key")
        assert plain_text != self.PLAIN_BLOB
