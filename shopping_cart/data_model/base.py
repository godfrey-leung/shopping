from typing import List

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from shopping_cart.exc import InstanceNotFound


Base = declarative_base()

_schema_version = 1


class QueryMixin:
    """
    Mixin object used to provide common functionality

    @DynamicAttrs
    """

    @classmethod
    def count(cls, session: Session) -> int:
        """
        The number of rows in the corresponding table
        """
        return session.query(cls).count()

    @classmethod
    def all(cls, session) -> List:
        """
        One instance of the class for each row in the table
        """
        return session.query(cls).all()


class ModelMixin(QueryMixin):
    """
    Mixin for objects that use an integer as their primary id
    """

    id = Column(Integer, primary_key=True)

    @classmethod
    def exists(
            cls,
            object_id: int,
            session: Session
    ) -> bool:
        """
        Check if an object exists in the database

        Parameters
        ----------
        object_id
            A database identifier for an object
        session
            A SQLAlchemy session

        Returns
        -------
            True iff an object of this class exists with the given id
        """
        return session.query(
            cls
        ).filter(
            cls.id == object_id
        ).count() > 0

    @classmethod
    def with_id(
            cls,
            object_id: int,
            session: Session
    ) -> "ModelMixin":
        """
        Return the instance in the database with a given ID

        Parameters
        ----------
        object_id
            A database identifier for an object
        session
            A SQLAlchemy session

        Returns
        -------
            Instance with the given id

        Raises
        ----------
        InstanceNotFound
            if an instance of the given ID is not found

        """

        try:
            return session.query(
                cls
            ).filter(
                cls.id == object_id
            ).one()
        except NoResultFound:
            raise InstanceNotFound(
                f"Instance with ID {object_id} is not found in the database"
            )
