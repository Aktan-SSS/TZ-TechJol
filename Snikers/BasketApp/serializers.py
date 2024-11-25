from rest_framework import serializers
from .models import UserBasket


class UserBasketSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(source='product.price', read_only=True)

    class Meta:
        model = UserBasket
        fields = ['id', 'product', 'total_price', 'added_at']
