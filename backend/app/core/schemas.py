from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

# Money/quantities travel as strings ("1234.50") so no float rounding ever happens in JSON.
DecimalStr = Annotated[Decimal, PlainSerializer(lambda d: str(d), return_type=str)]


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Page[T](ApiModel):
    items: list[T]
    total: int


class Timestamps(ApiModel):
    created_at: datetime
    updated_at: datetime


COMPLIANCE_DISCLAIMER = (
    "This content was extracted automatically to support tender preparation. It is not a "
    "ruling that a bid complies. Check every item against the source documents."
)
