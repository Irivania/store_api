from datetime import datetime, timezone
from decimal import Decimal
from bson import Decimal128
from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator


class BaseSchemaMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class OutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    def convert_decimal128(cls, data):
        for key, value in list(data.items()):
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))
        return data
