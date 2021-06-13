import pytest

from shopping_cart import data_model as model


@pytest.fixture(name="product")
def make_product():

    def _generate(
            product_id: int,
            name: str,
            price: float
    ):
        return model.Product(
            id=product_id,
            name=name,
            unit_price=price
        )

    return _generate


class TestDiscountOffer:
    """
    Test the discount offer class
    """

    def test_add_offers(self, product, session):
        """
        Test add an offer to the database

        """

        product_example = product(
            product_id=0,
            name='Soap',
            price=100
        )
        offer = model.DiscountOffer(
            id=0,
            product=product_example
        )
        session.add(offer)

        assert model.DiscountOffer.count(session) == 1
        assert model.DiscountOffer.exists(0, session) is True
        assert model.DiscountOffer.with_id(0, session) == offer

        # test the associated product is added as well
        assert model.Product.exists(0, session) is True
        assert model.Product.with_id(0, session) == product_example


    def test_add_offers(self, product, session):
        """
        Test add an offer to the database

        """


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