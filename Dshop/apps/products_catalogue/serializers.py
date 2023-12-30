def serialize_cart(cart):
    return {
        "total": cart.total,
        "count": cart.count,
        "items": [
            {
                "item_id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "price": item.price,
                "subtotal": item.subtotal,
                "quantity": item.quantity
            }
            for item in cart
        ]
    }