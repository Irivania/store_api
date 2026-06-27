from typing import Any, List
from uuid import UUID
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone
import pymongo
from bson import Decimal128
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException

def _convert_value_for_mongo(value: Any) -> Any:
    if isinstance(value, Decimal):
        return Decimal128(str(value))

    if isinstance(value, str):
        try:
            return Decimal128(str(Decimal(value)))
        except (InvalidOperation, ValueError):
            return value

    return value

def _convert_update_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {k: _convert_value_for_mongo(v) for k, v in payload.items()}

class ProductUsecase:
    def __init__(self) -> None:
        pass

    def _get_collection(self):
        database = db_client.get()
        return database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        if isinstance(body, dict):
            body = ProductIn(**body)
            
        product_model = ProductModel(**body.model_dump())
        collection = self._get_collection()
        await collection.insert_one(product_model.model_dump())
        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        collection = self._get_collection()
        result = await collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        return ProductOut(**result)

    async def query(
        self,
        limit: int = 10,
        offset: int = 0,
        name: str | None = None,
    ) -> List[ProductOut]:
        collection = self._get_collection()

        query_filter = {}
        if name:
            query_filter["name"] = {"$regex": name, "$options": "i"}

        cursor = (
            collection.find(query_filter)
            .sort("created_at", pymongo.DESCENDING)
            .skip(offset)
            .limit(limit)
        )

        return [ProductOut(**item) async for item in cursor]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        collection = self._get_collection()
        
        # Converte o body para dict ignorando campos None
        data = body.model_dump(exclude_none=True)
        
        # Adiciona o timestamp de atualização atual
        data["updated_at"] = datetime.now(timezone.utc)
        
        # Converte para os tipos compatíveis com o MongoDB
        data = _convert_update_payload(data)
        
        result = await collection.find_one_and_update(
            filter={"id": id},
            update={"$set": data},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
            
        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        collection = self._get_collection()
        product = await collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        result = await collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False

product_usecase = ProductUsecase()