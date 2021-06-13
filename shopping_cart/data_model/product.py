from abc import ABC, abstractmethod

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, Date, ForeignKey, func, Float, Boolean, DateTime, Table
)
from sqlalchemy.orm import relationship, Session

from shopping_cart.data_model.base import Base, ModelMixin


class Product(Base, ModelMixin):
    """
    A product available for selection
    """
    __tablename__ = "product"

    name = Column(String)
    unit_price = Column(Float)

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
    A discount offer associated to a product
    """
    __tablename__ = "discount_offer"

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


