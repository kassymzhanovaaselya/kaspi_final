from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from common.base_class import Base


@dataclass
class Commission(Base):
    type_code: str
    percentage: Decimal
