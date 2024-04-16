#!/usr/bin/env python

__doc__ = "Populates the DB with initial values"


from src.repository import db

from tests.factory.content import ContentFactory
from tests.factory.device import DeviceFactory
from tests.factory.protection_system import ProtectionSystemFactory


PROTECTION_SYSTEMS = [
    {"name": "AES 1", "encryption_mode": "AES+ECB"},
    {"name": "AES 2", "encryption_mode": "AES+CBC"},
]

CONTENTS = [
    {
        "protection_system_id": 2,
        "encryption_key": "KEY1",
        "encrypted_payload": "Content 1 Payload",
    },
    {
        "protection_system_id": 1,
        "encryption_key": "KEY2",
        "encrypted_payload": "Content 2 Payload",
    },
]

DEVICES = [
    {"name": "Android", "protection_system_id": 1},
    {"name": "Samsung", "protection_system_id": 2},
    {"name": "iOS", "protection_system_id": 1},
    {"name": "LG", "protection_system_id": 2},
]


def seed_db():
    db.init()

    for ps in PROTECTION_SYSTEMS:
        ProtectionSystemFactory.new(**ps)

    for cnt in CONTENTS:
        ContentFactory.new(**cnt)

    for device in DEVICES:
        DeviceFactory.new(**device)


if __name__ == "__main__":
    seed_db()
