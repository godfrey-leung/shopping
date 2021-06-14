from pathlib import Path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_cart import data_model as m
from shopping_cart.store.operations import populate

directory = Path(__file__).parent.parent


def make_new_store(
        product_config_path
):
    """
    Make a new store backend database and
    populate products from configuration yaml

    Returns
    -------
    product_config_path
        filepath of the product configuration file
    store
        store product database

    """
    engine = create_engine('sqlite://')

    m.Base.metadata.create_all(engine)
    store = sessionmaker(bind=engine)()

    with open(product_config_path) as f:
        product_dict = yaml.safe_load(f)

    populate(
        product_dict,
        store
    )

    return store
