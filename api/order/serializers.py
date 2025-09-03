from rest_framework import serializers
from content.models import Order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_customer(self, obj):
        if obj.customer:
            return {"id": obj.id, "name": getattr("obj.customer", "name", None)}

        return None
