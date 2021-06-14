#!/usr/bin/env python
from pathlib import Path

from scripts.make_store import make_new_store
from shopping_cart.shopping.cart import ShoppingCart

directory = Path(__file__).parent.parent


def main():

    store = make_new_store(directory / "files/stores/store_2.yaml")
    cart_1 = ShoppingCart(store=store)

    # add 2 Dove Soaps and 2 Axe Deos to the shopping cart
    cart_1.add_product_items(
        "Dove Soap", 3
    )

    product_list = {}
    for product, quantity in cart_1.product_list.items():
        product_list[product.name] = quantity

    breakdown_price = cart_1.price_breakdown(12.5)

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total discount: {breakdown_price['total_discount']}")
    print(f"Total tax amount: {breakdown_price['total_tax']}")
    print(f"Total price: {breakdown_price['total_price']}")

    cart_2 = ShoppingCart(store=store)
    # add 5 Dove Soaps to the shopping cart
    cart_2.add_product_items(
        "Dove Soap", 5
    )

    product_list = {}
    for product, quantity in cart_2.product_list.items():
        product_list[product.name] = quantity

    breakdown_price = cart_2.price_breakdown(12.5)

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total discount: {breakdown_price['total_discount']}")
    print(f"Total tax amount: {breakdown_price['total_tax']}")
    print(f"Total price: {breakdown_price['total_price']}")

    cart_3 = ShoppingCart(store=store)
    # add 3 Dove Soaps to the shopping cart
    cart_3.add_product_items(
        "Dove Soap", 3
    )
    cart_3.add_product_items(
        "Axe Deo", 2
    )

    product_list = {}
    for product, quantity in cart_3.product_list.items():
        product_list[product.name] = quantity

    breakdown_price = cart_3.price_breakdown(12.5)

    print("\nYour current shopping cart")
    print(f"Items in the cart: {product_list}")
    print(f"Total discount: {breakdown_price['total_discount']}")
    print(f"Total tax amount: {breakdown_price['total_tax']}")
    print(f"Total price: {breakdown_price['total_price']}")




if __name__ == "__main__":
    main()
