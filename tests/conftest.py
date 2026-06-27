import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from store.db.mongo import db_client
from store.usecases.product import product_usecase
from tests.factories import product_data, products_data
from store.schemas.product import ProductIn, ProductUpdate

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
async def mongo_client():
    db = db_client.get()
    yield db

@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    # Executa a limpeza ANTES do teste começar (sem finalizer)
    db = mongo_client
    collections = await db.list_collection_names()
    for col in collections:
        if not col.startswith("system"):
            await db[col].delete_many({})

@pytest.fixture
def products_url():
    return "/products/"

@pytest.fixture
async def client(clear_collections):
    from store.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def product_in():
    return ProductIn(**product_data())


@pytest.fixture
def product_up():
    return ProductUpdate()


@pytest.fixture
async def product_inserted(clear_collections):
    return await product_usecase.create(body=ProductIn(**product_data()))

@pytest.fixture
async def products_inserted(clear_collections):
    return [await product_usecase.create(body=ProductIn(**p)) for p in products_data()]
