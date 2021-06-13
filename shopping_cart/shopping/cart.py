from typing import Optional, List
from uuid import uuid4

from sqlalchemy.orm import Session

from shopping_cart.data_model.product import Item, Product
from shopping_cart.exc import InvalidAmount


class ShoppingCart:
    """

    """

    def __init__(
            self,
            store: Session,
            cart_id: Optional[int] = str(uuid4()),
            items: List[Item] = None
    ):
        """

        Parameters
        ----------
        store
            the store database
        cart_id
            identifier of the shopping cart. Default = str(uuid4())
        items
            items in the cart. Default = None

        """

        self.store = store
        self.cart_id = cart_id
        self.items = items

    def add_product_items(
            self,
            product_name: str,
            quantity: int,
            is_random: bool = False
    ):
        """
        Add N items of a given product to the cart

        Parameters
        ----------
        product_name
            the name of the product to be added
        quantity
            number of the product items to be added
        is_random
            If True, randomly pick the N
            available items from the store.
            Default = False

        """

        self.items.extend(
            Product.pick(
                self.store,
                product_name,
                quantity,
                is_random
            )
        )

    @property
    def total_marked_price(self) -> float:
        """
        Total marked price before discount of all the items
        in the cart

        """

        if self.items is None:
            return 0

        total = 0
        for item in self.items:
            total += item.product.unit_price

        return total

    @property
    def total_discount(self):

    def total_price_before_tax




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