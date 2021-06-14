#!/usr/bin/env python
from pathlib import Path

from shopping_cart.make_store import make_new_store
from shopping_cart.shopping.cart import ShoppingCart

directory = Path(__file__).parent.parent


def main():

    store = make_new_store(directory / "files/stores/store_4.yaml")
    cart = ShoppingCart(store=store)

    # add 5 Dove Soaps and 4 Axe Deos to the shopping cart
    cart.add_product_items(
        "Dove Soap", 5
    )
    cart.add_product_items(
        "Axe Deo", 4
    )

    product_list = {}
    for product, quantity in cart.product_list.items():
        product_list[product.name] = quantity

    breakdown_price = cart.price_breakdown(12.5, 500, 20)

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total discount: {breakdown_price['total_discount']}")
    print(f"Total tax amount: {breakdown_price['total_tax']}")
    print(f"Total price: {breakdown_price['total_price']}")


if __name__ == "__main__":
    main()
