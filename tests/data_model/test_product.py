import pytest

from shopping_cart.data_model.product import Product, DiscountOffer
from shopping_cart.exc import InvalidValue


@pytest.fixture(name="product")
def make_product():

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
        Test assigning invalid required quantity
        to the discount offer

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


class TestDiscountOffer:
    """
    Test the discount offer class
    """

    def test_invalid_required_quantity(self, session):
        """
        Test assigning invalid required quantity
        to the discount offer

        """

        with pytest.raises(InvalidValue) as exc_info:
            DiscountOffer(
                id=0,
                required_quantity=0,
                discount=50
            )

        expected_error_message = (
            "Required quantity must be a positive integer for promotion offer."
        )
        assert exc_info.match(expected_error_message)

    def test_invalid_discount(self, session):
        """
        Test assigning invalid discount percentage
        to the discount offer

        """

        with pytest.raises(InvalidValue) as exc_info:
            DiscountOffer(
                id=0,
                required_quantity=3,
                discount=120
            )

        expected_error_message = (
            "Discount percentage must be between 0 and 100."
        )
        assert exc_info.match(expected_error_message)

    def test_add_offers(self, product, session):
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
            discount=30,
            product=product_example
        )
        session.add(offer)

        assert DiscountOffer.count(session) == 1
        assert DiscountOffer.exists(0, session) is True
        assert DiscountOffer.with_id(0, session) == offer

        # test the associated product is added as well
        assert Product.exists(0, session) is True
        assert Product.with_id(0, session) == product_example


    # def test_add_offers(self, product, session):
    #     """
    #     Test add an offer to the database
    #
    #     """


#
# class TestProduct:
#     """
#     Test the product class
#     """
#
#     def test_add_products(self):
#         """
#         Test add products to the database
#
#         """
#
#         product_1 = model.Product(
#
#         )