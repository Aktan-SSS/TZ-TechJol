from django.test import TestCase
from django.contrib.auth.models import User
from ProductApp.models import Product
from .serializers import UserBasketSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserBasket


class UserBasketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(product_name='Test Product', price=100)
        self.basket_item = UserBasket.objects.create(user=self.user, product=self.product)

    def test_user_basket_str(self):
        self.assertEqual(str(self.basket_item), f"{self.user.username} - {self.product.product_name}")

    def test_total_price(self):
        self.assertEqual(self.basket_item.total_price(), self.product.price)

class UserBasketSerializerTest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(product_name='Test Product', price=100)
        self.user_basket = UserBasket.objects.create(user=User.objects.create_user(username='testuser'), product=self.product)

    def test_serialized_data(self):
        serializer = UserBasketSerializer(instance=self.user_basket)
        expected_data = {
            'id': self.user_basket.id,
            'product': self.product.id,
            'total_price': self.product.price,
            'added_at': self.user_basket.added_at.isoformat().replace('+00:00', 'Z'),
        }
        self.assertDictContainsSubset(expected_data, serializer.data)

class UserBasketViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(product_name='Test Product', price=100)

    def test_list_basket(self):
        UserBasket.objects.create(user=self.user, product=self.product)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('UserBasket', response.data)
        self.assertEqual(response.data['total_sum'], self.product.price)

    def test_add_to_basket_success(self):
        response = self.client.post('/api/cart/', {'product_id': self.product.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product'], self.product.id)

    def test_add_to_basket_product_not_found(self):
        response = self.client.post('/api/cart/', {'product_id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Продукт не найден')

    def test_remove_from_basket_success(self):
        basket_item = UserBasket.objects.create(user=self.user, product=self.product)
        response = self.client.delete(f'/api/cart/{basket_item.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_from_basket_not_found(self):
        response = self.client.delete('/api/cart/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Товар не найден в вашей корзине')
