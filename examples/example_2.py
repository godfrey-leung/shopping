#!/usr/bin/env python
from pathlib import Path

from scripts.make_store import make_new_store
from shopping_cart.shopping.cart import ShoppingCart

directory = Path(__file__).parent.parent


def main():

    store = make_new_store(directory / "files/stores/store_1.yaml")
    cart = ShoppingCart(store=store)

    # add 5 Dove Soaps to the shopping cart
    cart.add_product_items(
        "Dove Soap", 5
    )

    product_list = {}
    for product, quantity in cart.product_list.items():
        product_list[product.name] = quantity

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total price: {cart.total_price(0)}")

    # add another 3 Dove Soaps to the shopping cart
    cart.add_product_items(
        "Dove Soap", 3
    )
    product_list = {}
    for product, quantity in cart.product_list.items():
        product_list[product.name] = quantity

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total price: {cart.total_price(0)}")


if __name__ == "__main__":
    main()
