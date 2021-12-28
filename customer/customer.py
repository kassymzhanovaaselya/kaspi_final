from dataclasses import dataclass
from typing import List
from uuid import UUID

from common.base_class import Base


@dataclass
class Customer(Base):
    first_name: str
    last_name: str
    age: int

    def to_json(self) -> dict:
        return {
            "id": str(self.id_),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": int(self.age)
        }