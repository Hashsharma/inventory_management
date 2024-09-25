from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, Category  # Ensure these models are imported correctly


class ProductAPITests(APITestCase):
    def setUp(self):
        # Create a test user

        payload = {
            'email': 'ana@gmail.com',
            'password': 'anand123@'
        }
        # self.login_url = reverse('login')
        # response = self.client.post(self.login_url, payload)

        # self.user = User.objects.filter(email='ana@gmail.com').first()
        # self.token  = RefreshToken.for_user(self.user)
        self.token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3MjcwOTE3LCJpYXQiOjE3MjcyNjczMTcsImp0aSI6IjRhZjJmYmI4MmM4MDRmYjhiYzcyYWM4ZjJmNWFiYTM0IiwidXNlcl9pZCI6Mn0.wzpja8d7hYn1aSMJO1N7BtjlOw2b6FBZ0UWFwA5gceM"
  # Create a token for the user


        # Create a sample category
        # self.category = Category.objects.create(name='Test Category')

        # URLs
        self.product_list_url = reverse('product_list')  # Adjust according to your URL config
        self.product_add_url = reverse('product_add')  # Adjust according to your URL config
        self.product_detail_url = lambda pk: reverse('product_detail', args=[pk])

    def test_product_list_authenticated(self):
        """Test fetching the product list as an authenticated user."""
        response = self.client.get(self.product_list_url,
                                   HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_product_list_unauthenticated(self):
        """Test fetching the product list without authentication."""
        self.client.logout()
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_add_success(self):
        """Test adding a new product."""
        payload = {
            'product_name': 'Laptop Lenovo',
            'category': self.category.id,
            'product_quantity_in_stock': 10,
            'product_price': 100000,
            'product_desc': 'Laptop with i7'
        }
        response = self.client.post(self.product_add_url,
                                    data=payload,
                                    HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('product_name', response.data)

    def test_product_add_duplicate(self):
        """Test adding a duplicate product."""
        Product.objects.create(
            product_name='Duplicate Product',
            category=self.category,
            product_quantity_in_stock=10,
            product_price=50000,
            product_desc='Duplicate description.',
            user=self.user
        )
        payload = {
            'product_name': 'Duplicate Product',
            'category': self.category.id,
            'product_quantity_in_stock': 5,
            'product_price': 30000,
            'product_desc': 'Attempting to add a duplicate product.'
        }
        response = self.client.post(self.product_add_url, data=payload,
                                    HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_product_update_success(self):
        """Test updating an existing product."""
        product = Product.objects.create(
            product_name='Old Laptop',
            category=self.category,
            product_quantity_in_stock=10,
            product_price=100000,
            product_desc='Old Laptop Description',
            user=self.user
        )

        payload = {
            'product_name': 'Updated Laptop',
            'category': self.category.id,
            'product_quantity_in_stock': 20,
            'product_price': 120000,
            'product_desc': 'Updated Laptop with better specs'
        }
        response = self.client.put(self.product_detail_url(product.id),
                                   data=payload,
                                   HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], 'Updated Laptop')

    def test_product_update_not_found(self):
        """Test updating a non-existent product."""
        payload = {
            'product_name': 'Non-existent Product',
            'category': self.category.id,
            'product_quantity_in_stock': 20,
            'product_price': 120000,
            'product_desc': 'This product does not exist.'
        }
        response = self.client.put(self.product_detail_url(999),
                                   data=payload,
                                   HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_delete_success(self):
        """Test deleting an existing product."""
        product = Product.objects.create(
            product_name='Laptop to Delete',
            category=self.category,
            product_quantity_in_stock=5,
            product_price=50000,
            product_desc='This product will be deleted',
            user=self.user
        )
        response = self.client.delete(self.product_detail_url(product.id),
                                      HTTP_AUTHORIZATION='<your_token>')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'Product deleted successfully.')

    def test_product_delete_not_found(self):
        """Test deleting a non-existent product."""
        response = self.client.delete(self.product_detail_url(999),
                                      HTTP_AUTHORIZATION=f'{self.token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# To run the tests, use the following command in your terminal:
# python manage.py test <your_app_name>
