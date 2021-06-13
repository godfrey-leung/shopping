from abc import ABC, abstractmethod

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, Date, ForeignKey, func, Float, Boolean, DateTime, Table
)

from data_model.base import Base

class Position(Base, ModelMixin):
    __tablename__ = "product"

    name = Column(String)
    unit_price = Column(Float)
    discount_offer = Column()

    operations = relationship(
        "Operation",
        secondary=operation_positions
    )




class AbstractProduct(ABC):
    """
    Abstract base product class
    """

    def __init__(
            self,
            name: str,
            unit_price: float
    ):
        """

        Parameters
        ----------
        name
            name of the product
        unit_price
            marked price for one unit
        """
        self.name = name
        self.unit_price = unit_price

    @property
    @abstractmethod
    def offer(self):
        """

        """
        pass


class Product:
