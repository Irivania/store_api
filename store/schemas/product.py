from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field, field_serializer, field_validator
from store.schemas.base import BaseSchemaMixin, OutSchema


def convert_decimal_128(v):
    if isinstance(v, Decimal128):
        return Decimal(str(v))
    return v


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal_ = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutSchema):
    @field_validator("price", mode="before")
    def convert_price_decimal128(cls, value):
        if isinstance(value, Decimal128):
            return Decimal(str(value))
        return value

    @field_serializer("price")
    def serialize_price(self, value):
        if isinstance(value, (Decimal, Decimal128)):
            return str(value)
        return value


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductOut):
    ...
