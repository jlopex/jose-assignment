from src.service.crypto.drivers.aes_cbc import AesCbcDriver


class TestAesCbcDriver:
    PLAIN_BLOB = """¿Cómo podría yo introducir nuevos dioses por decir que una voz divina se me manifiesta para 
    indicarme lo que hay que hacer?""".encode(
        "utf-8"
    )

    CRYPTED_BLOB: bytes = (
        b"\x0f\xce\xa58\xd1}z\xd0Y\xd8thP?i`i\xb3\x8eh6\x17N\x1el\x11\xeda-\x93\x0e\xfdX[\xeaB\x18\x1a\x0b.\xae\xe9"
        b'\x8ap\xd1\x16"\xe2\x1b\xa4x\xf2\xa8\xbcW\x06\xf0\x83o\xc5\xcbpg\x18\xc1!\\\xeb\xe8\x98\xb8/k[\xef\xf5\x16'
        b"\x98\x88\xc67\xd2\xa6WX\\z\x9c\x9a:\xe0\x0e\xba\xb4F\xfc{\x19`\x14\x1e\xf6\xc7\xaaZ\x04e^b\x1f\x83\xc3"
        b"\xfdq%\xe3\xe5\xf0o\x9b\t\xc9\xc5\x8f\xa2\x16\x06\xab\xf5m!"
    )

    def test_crypt(self):
        crypted_text = AesCbcDriver.encrypt(self.PLAIN_BLOB, key="fake key")
        assert crypted_text == self.CRYPTED_BLOB

    def test_decrypt(self):
        plain_text = AesCbcDriver.decrypt(self.CRYPTED_BLOB, key="fake key")
        assert plain_text == self.PLAIN_BLOB

    def test_decrypt_with_invalid_key(self):
        plain_text = AesCbcDriver.decrypt(self.CRYPTED_BLOB, key="fake_key")
        assert plain_text != self.PLAIN_BLOB
