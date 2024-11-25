from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import ProductSerializer
from rest_framework import viewsets
from .models import Product
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilterSet
from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet
    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={
            201: "Продукт успешно создан",
            400: "Ошибка не правельные данные",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
