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
        self.items = items or []

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

        total = 0
        for item in self.items:
            total += item.product.unit_price

        return total

    def total_discount(
            self,
            required_purchase_total: Optional[float] = None,
            global_rate: Optional[float] = None
    ) -> float:
        """
        Total discount amount including individual product discounts and
        global discount, rounded off to the 2 decimal places

        Parameters
        ----------
        required_purchase_total
            required total cost of the purchase to get the global discount
        global_rate
            global discount rate

        Returns
        -------
        amount
            total discount amount

        """

        amount = 0
        for product, quantity in self.product_list.items():
            discount_offer = product.discount_offer
            if discount_offer is None:
                continue

            number_of_discounted_items = quantity // discount_offer.required_quantity
            amount += product.unit_price * number_of_discounted_items * discount_offer.percentage / 100

        # add global discount
        if required_purchase_total is not None:
            if required_purchase_total <= 0:
                raise InvalidValue(
                    f"The required total cost of the purchase for global discount must be positive. "
                    f"{required_purchase_total} is given instead."
                )

            if not 100 > global_rate > 0:
                raise InvalidValue(
                    f"Global discount rate must be between 0 and 100. {global_rate} is given instead."
                )

            price_after_product_discount = self.total_marked_price - amount
            if price_after_product_discount >= required_purchase_total:
                global_discount = price_after_product_discount * global_rate / 100
                amount += global_discount

        return round(amount, 2)

    def total_price_before_tax(
            self,
            required_purchase_total: Optional[float] = None,
            global_rate: Optional[float] = None
    ) -> float:
        """
        Total price before tax after discount

        Parameters
        ----------
        required_purchase_total
            required total cost of the purchase to get the global discount
        global_rate
            global discount rate

        """

        return self.total_marked_price - self.total_discount(
            required_purchase_total, global_rate
        )

    def total_tax_amount(
            self,
            tax_rate: float,
            required_purchase_total: Optional[float] = None,
            global_rate: Optional[float] = None
    ) -> float:
        """
        Total tax amount on total marked discounted price

        Parameters
        ----------
        tax_rate
            tax rate (in percentage) of the shopping cart
        required_purchase_total
            required total cost of the purchase to get the global discount
        global_rate
            global discount rate

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
            self.total_price_before_tax(
                required_purchase_total, global_rate
            ) * tax_rate / 100,
            1
        )

    def total_price(
            self,
            tax_rate: float,
            required_purchase_total: Optional[float] = None,
            global_rate: Optional[float] = None
    ) -> float:
        """
        Total price of the cart with discount subtracted
        and tax added, rounded off to 2 decimal places

        Parameters
        ----------
        tax_rate
            tax rate (in percentage) of the shopping cart
        required_purchase_total
            required total cost of the purchase to get the global discount
        global_rate
            global discount rate

        Returns
        -------
            total price

        """

        return round(
            self.total_price_before_tax(
                required_purchase_total, global_rate
            ) + self.total_tax_amount(
                tax_rate, required_purchase_total, global_rate
            ),
            2
        )

    def price_breakdown(
            self,
            tax_rate: float,
            required_purchase_total: Optional[float] = None,
            global_rate: Optional[float] = None
    ) -> dict:
        """
        Breakdown price of the cart in a dict including total discount,
        total tax amount and total price

        Parameters
        ----------
        tax_rate
            tax rate (in percentage) of the shopping cart
        required_purchase_total
            required total cost of the purchase to get the global discount
        global_rate
            global discount rate

        Returns
        -------
            breakdown price

        """

        return {
            "total_discount": self.total_discount(
                required_purchase_total, global_rate
            ),
            "total_tax": self.total_tax_amount(
                tax_rate, required_purchase_total, global_rate
            ),
            "total_price": self.total_price(
                tax_rate, required_purchase_total, global_rate
            )
        }
