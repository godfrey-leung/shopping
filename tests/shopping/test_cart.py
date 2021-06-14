import pytest

from shopping_cart.exc import InvalidValue
from shopping_cart.shopping.cart import ShoppingCart


@pytest.fixture(name="cart")
def make_empty_cart(store):
    """
    Pytest fixture to make an empty cart

    """
    return ShoppingCart(store=store)


class TestShoppingCart:
    """
    Test the shopping cart class
    """

    @pytest.mark.parametrize(
        "product_name",
        [
            "A", "B"
        ]
    )
    def test_add_product_items(
            self, product_name, cart
    ):
        """
        Test .add_product_items() method

        """

        assert len(cart.items) == 0

        cart.add_product_items(
            product_name, 3
        )
        assert len(cart.items) == 3

        cart.add_product_items(
            "C", 2
        )
        assert len(cart.items) == 5

    def test_product_list(
            self, cart
    ):
        """
        Test the product_list property

        """

        assert cart.product_list == {}

        cart.add_product_items(
            "C", 3
        )
        cart.add_product_items(
            "B", 1
        )

        product_list = {}
        for product, quantity in cart.product_list.items():
            product_list[product.name] = quantity

        assert product_list == {"B": 1, "C": 3}

    @pytest.mark.parametrize(
        "product_name, final_total",
        [
            ("B", 489.95),
            ("C", 289.97)
        ]
    )
    def test_total_marked_price(
            self, product_name, final_total, cart
    ):
        """
        Test the total_marked_price property

        """

        assert cart.total_marked_price == 0

        cart.add_product_items(
            "A", 3
        )
        assert cart.total_marked_price == 89.97

        cart.add_product_items(
            product_name, 2
        )
        assert round(cart.total_marked_price, 2) == final_total

    def test_total_discount_no_global(
            self, cart
    ):
        """
        Test the cart total discount, no global discount case

        """

        assert cart.total_discount() == 0

        cart.add_product_items(
            "C", 1
        )
        assert cart.total_discount() == 0

        cart.add_product_items(
            'A', 1
        )
        cart.add_product_items(
            "C", 1
        )
        assert cart.total_discount() == 100

    def test_total_discount_invalid_global(
            self, cart
    ):
        """
        Test the cart total discount with invalid global
        discount parameters

        """

        with pytest.raises(InvalidValue) as exc_info:
            cart.total_discount(0, 40)

        expected_error_message = (
            "The required total cost of the purchase for global discount must be positive. "
            "0 is given instead."
        )
        assert exc_info.match(expected_error_message)

        with pytest.raises(InvalidValue) as exc_info:
            cart.total_discount(1000, 100)

        expected_error_message = (
            f"Global discount rate must be between 0 and 100. 100 is given instead."
        )
        assert exc_info.match(expected_error_message)

    def test_total_discount_with_global(
            self, cart
    ):
        """
        Test the cart total discount with global discount

        """

        cart.add_product_items(
            'B', 10
        )
        cart.add_product_items(
            "C", 3
        )
        assert cart.total_discount(1000, 10) == 589.98

    @pytest.mark.parametrize(
        "required_purchase, expected_amount",
        [
            (600, 499.9),
            (400, 449.91)
        ]
    )
    def test_total_price_before_tax(
            self, cart, required_purchase, expected_amount
    ):
        """
        Test the cart total_price_before_tax property

        """

        cart.add_product_items(
            'A', 10
        )
        cart.add_product_items(
            "C", 3
        )
        assert round(cart.total_price_before_tax(), 2) == 499.9

        # with global discount
        assert round(
            cart.total_price_before_tax(
                required_purchase, 10
            ),
            2
        ) == expected_amount

    def test_total_tax_amount_invalid(
            self, cart
    ):
        """
        Test the cart total tax with invalid tax rate

        """

        with pytest.raises(InvalidValue) as exc_info:
            cart.total_tax_amount(-10)

        expected_error_message = "Tax rate must be non-negative. -10 is given."
        assert exc_info.match(expected_error_message)

    def test_total_tax_amount(
            self, cart
    ):
        """
        Test the cart total tax

        """

        cart.add_product_items(
            "C", 3
        )
        assert cart.total_tax_amount(5) == 10

    def test_total_tax_price(
            self, cart
    ):
        """
        Test the cart total price

        """

        cart.add_product_items(
            "C", 5
        )
        assert cart.total_price(5) == 315
