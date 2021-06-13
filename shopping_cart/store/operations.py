from copy import deepcopy
from itertools import count
import logging

from sqlalchemy.orm import Session

from shopping_cart import data_model as m

logger = logging.getLogger(__name__)


_default_product_id = count()
_default_offer_id = count()
_default_item_id = count()


def populate(
        model_dict: dict,
        session: Session
):
    """
    Parse product data from YAML and add it to the store database

    Parameters
    ----------
    model_dict
        store products configuration data
    session
        store product database

    """
    model_dict = deepcopy(model_dict)

    for product in model_dict["products"]:

        logger.info(f'Adding product {product["name"]}')

        # Promotion offer associated to the product
        promotion_offer = None
        if "promotion" in product:
            promotion = product["promotion"]
            promotion_offer = m.DiscountOffer(
                id=next(_default_offer_id),
                required_quantity=promotion["required_quantity"],
                percentage=promotion["percentage"]
            )

        product_instance = m.Product(
            id=next(_default_product_id),
            name=product["name"],
            unit_price=product["unit_price"],
            discount_offer=promotion_offer
        )

        for _ in range(product["number_in_store"]):
            session.add(
                m.Item(
                    id=next(_default_item_id),
                    product=product_instance
                )
            )

    session.commit()
