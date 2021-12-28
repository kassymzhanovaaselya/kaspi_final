from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Base:
    id_: Optional[UUID]