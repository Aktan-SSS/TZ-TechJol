from django.urls import path
from .views import UserBasketViewSet


urlpatterns = [
    path('api/cart/', UserBasketViewSet.as_view({'get': 'list', 'post': 'create'}, name='cart')),
    path('api/cart/<int:pk>/', UserBasketViewSet.as_view({'delete': 'destroy'}, name='cart-delete'))
]