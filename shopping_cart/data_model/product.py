from abc import ABC, abstractmethod

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, Date, ForeignKey, func, Float, Boolean, DateTime, Table
)
from sqlalchemy.orm import relationship, Session, validates

from shopping_cart.data_model.base import Base, ModelMixin
from shopping_cart.exc import InvalidValue


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
    discount = Column(Float)

    @validates('required_quantity')
    def validate_required_quantity(self, key, value):
        if value <= 0:
            raise InvalidValue(
                "Required quantity must be a positive integer for promotion offer."
            )

        return value

    @validates('discount')
    def validate_discount(self, key, value):
        if not 100 > value > 0:
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
    """
    __tablename__ = "item"

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

    # def purchase_price(
    #         self
    # ):


