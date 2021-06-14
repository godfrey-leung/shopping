from pathlib import Path
import pytest
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_cart import data_model as m
from shopping_cart.store.operations import populate


directory = Path(__file__).parent


@pytest.fixture(name="session")
def make_store_session():
    """
    Make a new empty store database session

    """
    engine = create_engine('sqlite://')
    session = sessionmaker(bind=engine)()
    m.Base.metadata.create_all(engine)
    yield session
    session.close()


@pytest.fixture(name="product")
def make_product():
    """
    Pytest fixture to generate a product instance

    """

    def _generate(
            product_id: int,
            name: str,
            price: float
    ):
        return m.Product(
            id=product_id,
            name=name,
            unit_price=price
        )

    return _generate


@pytest.fixture(name="store")
def make_store_database(session):
    """
    Pytest fixture to add list of products
    to the store database from a mock store configuration

    """

    with open(directory / "mock_data/store.yaml") as f:
        product_dict = yaml.safe_load(f)

    populate(
        product_dict,
        session
    )

    return session
