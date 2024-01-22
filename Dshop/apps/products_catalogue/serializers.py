from rest_framework import serializers

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

"""
example input
{items: [
    {product_id: 1, quantity: 100},
    {product_id: 10, quamtity: 600}]
}

example output
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

"""


class CartItemSerializer(serializers.Serializer):
    product_pk = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    product_name = serializers.CharField(read_only=True, max_length=200)
    price = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    subtotal = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    item_id = serializers.IntegerField(read_only=True, min_value=1)

    # zapewne będziesz tutaj musial napisac wlasne: to_internal_value albo lepiej create i update
    # https://www.django-rest-framework.org/api-guide/serializers/#baseserializer
    # aczkolwiek może warto będzie zrobić create i update w CartSerializer, zamiast tutaj.
    # Dlaczego? Bo tam masz bez problemu dostęp do pełnego cart.
    # Niemniej, zachowaj ten serializer do walidacji danych.


class CartSerializer(serializers.Serializer):
    total = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    items = CartItemSerializer(many=True, write_only=True)
    items = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True, min_value=1)

    def get_items(self, obj):
        print("alamakota get_items")
        print(obj)
        return "ala"  # co tu zwrócisz będzie w items
        # dokumentacja: https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

    def validate_items(self, items):
        item_ids = set()
        for item in items:
            item_id = item.get("item_id")
            if item_id in item_ids:
                raise serializers.ValidationError(
                    "item_id must be unique within items."
                )
            item_ids.add(item_id)
        return items
