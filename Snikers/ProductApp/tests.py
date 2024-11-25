from django.test import TestCase
from .serializers import ProductSerializer
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name="Test Product",
            brand="Test Brand",
            category="Test Category",
            price=1000
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "Test Product")
        self.assertEqual(self.product.price, 1000)
        self.assertEqual(str(self.product), "Test Product - 1000")


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product_data = {
            "product_name": "Test Product",
            "brand": "Test Brand",
            "category": "Test Category",
            "price": 1000
        }
        self.product = Product.objects.create(**self.product_data)

    def test_serializer_valid_data(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["product_name"], "Test Product")

    def test_serializer_invalid_data(self):
        invalid_data = self.product_data.copy()
        invalid_data["price"] = -100
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")        
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        self.product = Product.objects.create(
            product_name="Test Product",
            brand="Test Brand",
            category="Test Category",
            price=1000
        )
        
        self.product_data = {
            "product_name": "New Product",
            "brand": "New Brand",
            "category": "New Category",
            "price": 2000
        }

    def test_create_product_success(self):
        response = self.client.post('/api/products/', self.product_data)
        self.assertEqual(response.status_code, 201)
        
    def test_create_product_invalid_data(self):
        invalid_data = {"product_name": "", "brand": "", "category": "", "price": -10}
        response = self.client.post('/api/products/', invalid_data)
        self.assertEqual(response.status_code, 400)
