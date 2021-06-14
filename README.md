# shopping cart backend service

This simple python project is a solution to the Shopping Cart interview question at QoKoon.

The goal is to build a backend service that supports a shopping platform or a cashier system which provides
a detailed price breakdown of any shopping carts during checkout. The service should identify the unit price of a product,
what products and their corresponding quantities are in the cart, detailed price breakdown (i.e. total discount,
total tax amount and total price) of the cart.

Promotion discount offer type considered are "Buy N, get Y % off for the next item" (Buy 1 get 1 free is a special case example)
and "Get X % off if total purchase >= Z".


# Project top-level directory structure

    ├── examples                    # config yaml file
        ├── __init__.py
        ├── ...                     # explicit examples
    ├── files                       # config yaml files
        ├── stores
            ├── ...                 # example of store product config yaml files
    ├── requirements.txt            # python packages required
    ├── README.md
    ├── scripts                     # scripts for populating (mock) data and starting Docker & database
        ├── ...
    ├── shopping_cart               # main project folder
        ├── data_model              # store product warehouse SQL database model
            ├── __init__.py
            ├── base.py             # base classes with common functionalities
            ├── product.py          # classes related to a product, i.e. Product, DiscountOffer, Item
        ├── shopping
            ├── __init__.py
            ├── base.py             # shopping cart class
        ├── store
            ├── __init__.py
            ├── operations.py       # store warehouse database operations, i.e. populate products from config
        ├── __init__.py
        ├── make_store.py           # make a new store warehouse database
        ├── exc.py                  # exceptions
    ├── tests                       # Automated unit test files
        ├── mock_data
            ├── store.yaml          # mock store product config yaml file
        ├── ...


# Requirements

See requirements.txt for the package dependencies. To compile, run and manage the project, Poetry must be installed.
See https://python-poetry.org/docs/cli/ for further information

# Command

To install the package, run

```bash
poetry install
```

To run the unit tests, use the following commands

```bash
poetry run pytest
```

# Examples

Explicit examples (as stated in the test) can be found under the `/examples` directory. To run the example, run
```bash
python ./examples/example_{x}.py
```


# Product Warehouse Database schema

Below is the store product warehouse database model schema

### Product
        ├── id                          (primary key, integer)
        ├── name                        (name of the product, string)
        ├── unit_price                  (price of a single item unit, float)
    ├──linked & backpopulate
        ├── discount_offer_id           (associated promotion offer ID, integer)
        ├── discount_offer              (associated "Buy N, get Y % on next item" promotion offer)

### DiscountOffer, i.e. "Buy N, get Y % on next item" promotion offer
        ├── id                          (primary key, integer)
        ├── required_quantity           (required quantity to get the offer N+1, integer)
        ├── percentage                  (unit item discount rate, float)
    ├──linked & backpopulate
        ├── product_id                  (associated product ID, integer)
        ├── product                     (associated product)

### Item
        ├── id                          (primary key, integer)
        ├── is_available                (whether the item is available or not, boolean)
    ├──linked & backpopulate
        ├── product_id                  (associated product ID, integer)
        ├── product                     (associated product)


# Future Improvements

While the current version provides a simple backend to support a (e-)shopping platform, following future improvements
will be considered in order to make this backend service more practical and powerful such that can be deployed in a
real-world scenarios

### shopping cart
- add method to remove items from a shopping cart
- add method to empty a shopping cart
- add method to checkout a cart (and simultaneously change the cart items in the database to unavailable)

### product database
- add more attribute columns for a product, e.g. product type, brand
- allow multiple offers associated to a product
- add created timestamp attributes to allow future audit and analytics purposes
- add more attribute columns for an item, e.g. expiration date
- add product database version control, e.g. using migration tools such as alembic


# License

This project is developed by Godfrey Leung. For more details, please refer to the license.