from shopping_cart import data_model as m

from sqlalchemy.orm import Session


class TestPopulate:
    """
    Test the populate function for store operation
    """

    def test_store_session(
            self,
            store: Session
    ):
        """
        Test a store session example after populate

        Parameters
        ----------
        store
            a mock store

        """

        # Test products in the store
        assert m.Product.count(store) == 3

        products = m.Product.all(store)
        assert [product.name for product in products] == ['A', 'B', 'C']
        assert [product.unit_price for product in products] == [29.99, 199.99, 100]
        assert [len(product.items) for product in products] == [30, 20, 10]
        assert [
            product.discount_offer is not None
            for product in products
        ] == [False, True, True]

        # Test promotion offers
        assert m.DiscountOffer.count(store) == 2

        product_B = m.Product.with_name(store, 'B')
        assert product_B.discount_offer.required_quantity == 3
        assert product_B.discount_offer.percentage == 50

        product_C = m.Product.with_name(store, 'C')
        assert product_C.discount_offer.required_quantity == 2
        assert product_C.discount_offer.percentage == 100

        # Test items
        assert m.Item.count(store) == 60
