from typing import Optional, List
from uuid import uuid4

from shopping_cart.data_model.product import Item
from shopping_cart.exc import InvalidAmount


class ShoppingCart:
    """

    """

    def __init__(
            self,
            cart_id: Optional[int] = str(uuid4()),
            items: List[Item] = None,
            total_price: float = 0,
            total_discount: float = 0,
            total_tax: float = 0
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

        if total_discount >= total_price:
            raise InvalidAmount(
                "Total discount cannot be greater than the total price."
            )

        self.total_price = total_price
        self.total_discount = total_discount
        self.total_tax = total_tax



    # def add(
    #         self,
    #
    # ):