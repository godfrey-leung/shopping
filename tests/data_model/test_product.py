import pytest
import random

from shopping_cart.data_model.product import Product, DiscountOffer, Item
from shopping_cart.exc import InvalidValue, OverDemand, InstanceNotFound


@pytest.fixture(autouse=True)
def fix_random_seed():
    random.seed(42)


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
        return Product(
            id=product_id,
            name=name,
            unit_price=price
        )

    return _generate


class TestProduct:
    """
    Test the product class
    """

    def test_invalid_unit_price(self, session):
        """
        Test assigning invalid unit price to
        a product

        """

        with pytest.raises(InvalidValue) as exc_info:
            Product(
                id=0,
                unit_price=-100
            )

        expected_error_message = (
            "Unit price of a product must be positive."
        )
        assert exc_info.match(expected_error_message)

    def test_add_product(self, product, session):
        """
        Testing adding a product to the database

        """

        session.add(
            product(
                product_id=0,
                name='Shampoo',
                price=50
            )
        )

        assert Product.exists(0, session) is True

        queried_product = Product.with_id(0, session)

        assert queried_product.id == 0
        assert queried_product.name == 'Shampoo'
        assert queried_product.unit_price == 50
        assert queried_product.discount_offer is None

    def test_with_name(self, product, session):
        """
        Test .with_name() method

        """

        toothpaste = product(
            product_id=0,
            name='Toothpaste',
            price=20.5
        )
        session.add(toothpaste)

        assert Product.with_name(session, 'Toothpaste') == toothpaste

    def test_with_name_not_found(self, session):
        """
        Test .with_name() method when the given product name
        is not in the database

        """

        with pytest.raises(InstanceNotFound) as exc_info:
            Product.with_name(session, 'Toothbrush')

        expected_error_message = (
            f"Product Toothbrush not found."
        )
        assert exc_info.match(expected_error_message)

    @pytest.mark.parametrize(
        "is_random, item_ids",
        [
            (True, [2, 1, 5]),
            (False, [1, 2, 3])
        ]
    )
    def test_pick(self, product, session, is_random, item_ids):
        """
        Test .pick() method

        """

        product_example = product(
            product_id=0,
            name='C',
            price=40
        )

        for i in range(10, 0, -1):
            session.add(
                Item(
                    id=i,
                    product=product_example
                )
            )

        items = Product.pick(session, 'C', 3, is_random=is_random)
        assert len(items) == 3
        assert [item.id for item in items] == item_ids

    def test_invalid_quantity(self, session):
        """
        Test invalid request quantity when calling .pick() method

        """

        session.add(
            Product(
                id=0,
                name='B'
            )
        )

        with pytest.raises(InvalidValue) as exc_info:
            Product.pick(session, 'B', -1)

        expected_error_message = (
            f"Quantity request must be positive."
        )
        assert exc_info.match(expected_error_message)

    def test_over_demand(self, session):
        """
        Test excess request when calling .pick() method

        """

        session.add(
            Product(
                id=0,
                name='B'
            )
        )

        with pytest.raises(OverDemand) as exc_info:
            Product.pick(session, 'B', 5)

        expected_error_message = (
            f"Excess demand request. Only 0 is available, but 5 is requested."
        )
        assert exc_info.match(expected_error_message)


class TestDiscountOffer:
    """
    Test the discount offer class
    """

    def test_invalid_required_quantity(self, session):
        """
        Test assigning invalid required quantity
        to a discount offer

        """

        with pytest.raises(InvalidValue) as exc_info:
            DiscountOffer(
                id=0,
                required_quantity=0,
                percentage=50
            )

        expected_error_message = (
            "Required quantity must be a positive integer for promotion offer."
        )
        assert exc_info.match(expected_error_message)

    def test_invalid_discount(self, session):
        """
        Test assigning invalid discount percentage
        to a discount offer

        """

        with pytest.raises(InvalidValue) as exc_info:
            DiscountOffer(
                id=0,
                required_quantity=3,
                percentage=120
            )

        expected_error_message = (
            "Discount percentage must be between 0 and 100, including 100 but not 0."
        )
        assert exc_info.match(expected_error_message)

    def test_add_offer(self, product, session):
        """
        Test add an offer to the database

        """

        product_example = product(
            product_id=0,
            name='Soap',
            price=100
        )
        offer = DiscountOffer(
            id=0,
            required_quantity=4,
            percentage=30,
            product=product_example
        )
        session.add(offer)

        assert DiscountOffer.count(session) == 1
        assert DiscountOffer.exists(0, session) is True
        assert DiscountOffer.with_id(0, session) == offer

        # test the associated product is added as well
        assert Product.exists(0, session) is True
        assert Product.with_id(0, session) == product_example


class TestItem:
    """
    Test the item class
    """

    def test_add_item(self, product, session):
        """
        Test add an item to the database

        """

        product_example = product(
            product_id=0,
            name='A',
            price=30
        )

        session.add(
            Item(
                id=0,
                product=product_example
            )
        )

        assert Item.count(session) == 1
        assert Item.exists(0, session) is True

        # Check if associated product is added
        assert Product.exists(0, session) is True

        queried_product = Product.with_id(0, session)
        assert len(queried_product.items) == 1
        assert queried_product.name == 'A'
