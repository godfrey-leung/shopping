

class InstanceNotFound(Exception):
    """
    Raise if an instance is not found in
    the database
    """


class InvalidValue(Exception):
    """
    Raise if an invalid value is assigned to
    an instance column in the datase
    """


class OverDemand(Exception):
    """
    Raise if excess demand is requested
    """


class InvalidAmount(Exception):
    """
    Raise if an invalid total/tax/discount amount
    is assigned to a shopping cart
    """