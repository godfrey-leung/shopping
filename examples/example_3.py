#!/usr/bin/env python
from pathlib import Path

from scripts.make_store import make_new_store
from shopping_cart.shopping.cart import ShoppingCart

directory = Path(__file__).parent.parent


def main():

    store = make_new_store(directory / "files/stores/store_1.yaml")
    cart = ShoppingCart(store=store)

    # add 2 Dove Soaps and 2 Axe Deos to the shopping cart
    cart.add_product_items(
        "Dove Soap", 2
    )
    cart.add_product_items(
        "Axe Deo", 2
    )

    product_list = {}
    for product, quantity in cart.product_list.items():
        product_list[product.name] = quantity

    breakdown_price = cart.price_breakdown(12.5)

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total tax amount: {breakdown_price['total_tax']}")
    print(f"Total price: {breakdown_price['total_price']}")


if __name__ == "__main__":
    main()
