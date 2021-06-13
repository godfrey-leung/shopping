import operator
import random
from typing import List

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, Date, ForeignKey, func, Float, Boolean, DateTime, Table
)
from sqlalchemy.orm import relationship, Session, validates
from sqlalchemy.orm.exc import NoResultFound

from shopping_cart.data_model.base import Base, ModelMixin
from shopping_cart.exc import InvalidValue, OverDemand, InstanceNotFound


class Product(Base, ModelMixin):
    """
    A product available for selection

    Attributes
    ----------
    name
        name of the product
    unit_price
        marked price of a single item
    items
        List of corresponding items in store
    discount_offer
        associated promotion discount offer

    """
    __tablename__ = "product"

    name = Column(String, unique=True)
    unit_price = Column(Float)

    @validates('unit_price')
    def validate_unit_price(self, key, value):
        if value <= 0:
            raise InvalidValue(
                "Unit price of a product must be positive."
            )

        return value

    items = relationship(
        "Item",
        back_populates="product"
    )

    # Associated discount offer, can be None
    discount_offer_id = Column(
        Integer,
        ForeignKey(
            "product.id"
        )
    )
    discount_offer: "DiscountOffer" = relationship(
        "DiscountOffer",
        uselist=False,
        back_populates="product"
    )

    @classmethod
    def with_name(
            cls,
            session: Session,
            name: str
    ) -> "Product":
        """
        Query a product with the given name from
        a store database

        Parameters
        ----------
        session
            a store database
        name
            name of the product

        Returns
        -------
            product of the given name

        Raises
        ------
        InstanceNotFound
            If the product name is not found

        """

        try:
            return session.query(
                cls
            ).filter(
                cls.name == name
            ).one()
        except NoResultFound:
            raise InstanceNotFound(
                f"Product {name} not found."
            )

    @classmethod
    def pick(
            cls,
            session: Session,
            name: str,
            quantity: int,
            is_random: bool = False
    ) -> List["Item"]:
        """
        Pick N available items from the store database

        Parameters
        ----------
        session
            A store database session
        name
            name of the parent product
        quantity
            number of quantity to pick
        is_random
            If True, randomly pick the N
            available items from the database.
            Default = False

        Returns
        -------
            list of picked items

        Raises
        ------
        InvalidValue
            If the request quantity is non-positive
        OverDemand
            If request to pick more items than what is available
            in the database

        """

        if quantity <= 0:
            raise InvalidValue(
                "Quantity request must be positive."
            )

        product = cls.with_name(session, name)
        items_available = [
            item for item in product.items
            if item.is_available
        ]
        items_available = sorted(
            items_available,
            key=operator.attrgetter('id')
        )

        if len(items_available) < quantity:
            raise OverDemand(
                f"Excess demand request. Only "
                f"{len(items_available)} is available, but {quantity} is requested."
            )

        if is_random:
            return random.sample(items_available, quantity)

        return items_available[:quantity]


class DiscountOffer(Base, ModelMixin):
    """
    A "Buy N, Get Y % off for the next one" discount offer
    associated to a product

    Attributes
    ----------
    required_quantity
        purchase quantity required to get the promotion,
        i.e. the quantity N in "Buy N, Get Y % off for the next one"
    discount
        discount offer in the promotion, i.e. the percent Y in \
        "Buy N, Get Y % off for the next one"

    """
    __tablename__ = "discount_offer"

    required_quantity = Column(Integer)
    percentage = Column(Float)

    @validates('required_quantity')
    def validate_required_quantity(self, key, value):
        if value <= 0:
            raise InvalidValue(
                "Required quantity must be a positive integer for promotion offer."
            )

        return value

    @validates('percentage')
    def validate_discount(self, key, value):
        if not 100 > value >= 0:
            raise InvalidValue(
                "Discount percentage must be between 0 and 100."
            )

        return value

    product_id = Column(
        Integer,
        ForeignKey(
            "product.id"
        )
    )
    product: "Product" = relationship(
        "Product",
        uselist=False,
        back_populates="discount_offer"
    )


class Item(Base, ModelMixin):
    """
    A specific product item

    Attributes
    ----------
    is_available
        Whether the item is available
    product
        what product the item is

    """
    __tablename__ = "item"

    is_available = Column(Boolean, default=True)

    product_id = Column(
        Integer,
        ForeignKey(
            "product.id"
        )
    )
    product: "Product" = relationship(
        "Product",
        uselist=False,
        back_populates="items"
    )

