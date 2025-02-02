import dataclasses
import os

from pymongo import MongoClient


port = int(os.environ.get("MONGODB_PORT", 27017))
user = os.environ.get("MONGODB_USER")
pwd = os.environ.get("MONGODB_PASS")

db = os.environ.get("MONGODB_DB", 'shiphero')
client = MongoClient(f"mongo:{port}", username=user, password=pwd)
project_db = client[db]


@dataclasses.dataclass
class Order:
    order_number: int    # NTH: make it automatically unique?
    name: str
    city: str
    state: str
    postal_code: str
    address1: str
    weight: int = 1
    address2: str = ""

    @classmethod
    def load(cls, order_number):
        return cls(**project_db.orders.find_one({"order_number": order_number}))

    def persist(self):
        project_db.orders.insert_one(dataclasses.asdict(self))