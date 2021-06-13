from typing import Optional, List
from uuid import uuid4

from shopping_cart.data_model.product import Item


class ShoppingCart:
    """

    """

    def __init__(
            self,
            cart_id: Optional[int] = str(uuid4()),
            items: List[Item] = None
    ):
        """

        Parameters
        ----------
        cart_id
            identifier of the shopping cart. Default = str(uuid4())
        items

        """

        self.cart_id = cart_id
        self.items = items

    # def add(
    #         self,
    #
    # ):