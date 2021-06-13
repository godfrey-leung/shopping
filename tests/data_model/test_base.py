import pytest

from sqlalchemy import Column, Integer, String

from shopping_cart.data_model.base import Base, QueryMixin, ModelMixin
from shopping_cart.exc import InstanceNotFound


class QueryBaseExample(Base, QueryMixin):
    """
    A queryable base instance for testing
    """
    __tablename__ = "query_base_example"

    name = Column(String, primary_key=True)


class ModelBaseExample(Base, ModelMixin):
    """
    A data model base instance for testing
    """
    __tablename__ = "model_base_example"


@pytest.fixture(name="query_mixin")
def make_query_mixin():
    """
    Pytest fixture for making a queryable base
    instance example with a given name

    """

    def _generate(
            name: str
    ):
        return QueryBaseExample(name=name)

    return _generate


@pytest.fixture(name="model_mixin")
def make_model_mixin():
    """
    Pytest fixture for making a model base
    instance example with a numeric ID

    """

    def _generate(
            exmample_id: int
    ):
        return ModelBaseExample(id=exmample_id)

    return _generate


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
        Test the .count() class method of QueryMixin

        """

        for i in range(number_to_add):
            session.add(
                query_mixin(
                    name=str(i)
                )
            )

        number_of_query_mixins = QueryBaseExample.count(session)
        assert number_of_query_mixins == number_to_add

    def test_all(self, query_mixin, session):
        """
        Test the .all() class method of QueryMixin

        """

        instance_1 = query_mixin(name='A')
        instance_2 = query_mixin(name='B')

        session.add(instance_1)
        session.add(instance_2)

        assert QueryBaseExample.all(session) == [instance_1, instance_2]


class TestModelMixin:
    """
    Test ModelMixin database base class
    """

    def test_exists(self, model_mixin, session):
        """
        Test the .exists() class method of ModelMixin

        """

        assert ModelBaseExample.exists(0, session) is False

        session.add(
            model_mixin(exmample_id=0)
        )

        assert ModelBaseExample.exists(0, session) is True

    def test_with_id(self, model_mixin, session):
        """
        Test the .with_id() class method of ModelMixin

        """

        instance = model_mixin(exmample_id=1)
        session.add(instance)

        queried_instance_with_id = ModelBaseExample.with_id(1, session)
        assert queried_instance_with_id == instance
        assert isinstance(queried_instance_with_id, QueryMixin) is True

    def test_with_id_absent(self, session):
        """
        Test the .with_id() class method of ModelMixin
        when the instance with the given ID is absent

        """

        with pytest.raises(InstanceNotFound) as exc_info:
            ModelBaseExample.with_id(1, session)

        expected_message = "Instance with ID 1 is not found in the database"
        assert exc_info.match(expected_message)
