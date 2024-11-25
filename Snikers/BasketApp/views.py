from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserBasket
from .serializers import UserBasketSerializer
from ProductApp.models import Product
from drf_yasg.utils import swagger_auto_schema


class UserBasketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBasket.objects.all()
    serializer_class = UserBasketSerializer

    @swagger_auto_schema(responses={200: UserBasketSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        basket_items = UserBasket.objects.filter(user=request.user)
        serializer = UserBasketSerializer(basket_items, many=True)
        total_sum = sum(item['total_price'] for item in serializer.data)
        return Response({"UserBasket": serializer.data, "total_sum": total_sum}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserBasketSerializer, responses={201: UserBasketSerializer})
    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "Введите id продукта в полу 'product_id'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Продукт не найден"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = UserBasket.objects.get_or_create(user=request.user, product=product)
        serializer = UserBasketSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={204: "Удалено"})
    def destroy(self, request, *args, **kwargs):
        try:
            basket_item = UserBasket.objects.get(user=request.user, product_id=kwargs.get('pk'))
            basket_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserBasket.DoesNotExist:
            return Response({"error": "Товар не найден в вашей корзине"}, status=status.HTTP_404_NOT_FOUND)
