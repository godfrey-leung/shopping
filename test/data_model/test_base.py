import pytest

from shopping_cart import data_model as model


class TestQueryMixin:
    """
    Test QueryMixin database base class
    """

    @pytest.mark.parametrize(
        "number_to_add",
        [
            0, 10, 100
        ]
    )
    def test_count(self, query_mixin, session, number_to_add):
        """
        Test the count method of QueryMixin

        """

        assert model.QueryMixin.count(session) == 0

        for _ in range(number_to_add):
            session.add(query_mixin)

        number_of_query_mixins = model.QueryMixin.count(session)
        assert number_of_query_mixins == number_to_add

