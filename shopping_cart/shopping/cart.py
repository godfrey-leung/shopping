from collections import defaultdict
from typing import Optional, List
from uuid import uuid4

from sqlalchemy.orm import Session

from shopping_cart.data_model.product import Item, Product
from shopping_cart.exc import InvalidValue


class ShoppingCart:
    """
    A shopping cart
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
    def product_list(self) -> dict:
        """
        A dictionary of the products and their corresponding quantity
        in the cart

        """

        products = defaultdict(int)
        for item in self.items:
            products[item.product] += 1

        return products

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
    def total_discount(self) -> float:
        """
        Total discount amount, rounded off to the
        2 decimal places

        """

        if self.items is None:
            return 0

        amount = 0
        for product, quantity in self.product_list.items():
            discount_offer = product.discount_offer
            if discount_offer is None:
                continue

            number_of_discounted_items = quantity // discount_offer.required_quantity
            amount += product.unit_price * number_of_discounted_items * discount_offer.percentage
        return round(amount, 2)

    @property
    def total_price_before_tax(self) -> float:
        """
        Total price before tax

        """

        return self.total_marked_price - self.total_discount

    def total_tax_amount(
            self,
            tax_rate: float
    ) -> float:
        """
        Total tax amount on total marked discounted price

        Parameters
        ----------
        tax_rate
            tax rate (in percentage) of the shopping cart

        Returns
        -------
            total tax amount

        Raises
        ------
        InvalidValue
            If the given tax rate is negative

        """

        if tax_rate < 0:
            raise InvalidValue(
                f"Tax rate must be non-negative. {tax_rate} is given."
            )

        return round(
            self.total_price_before_tax * tax_rate / 100,
            2
        )

    def total_price(
            self,
            tax_rate: float
    ) -> float:
        """
        Total price of the cart with discount subtracted
        and tax added, rounded off to 2 decimal places

        Parameters
        ----------
        tax_rate
            tax rate (in percentage) of the shopping cart

        Returns
        -------
            total price

        """

        return round(
            self.total_price_before_tax - self.total_tax_amount(tax_rate),
            2
        )
