# import unittest
# import requests
#
# BASE_URL = 'http://127.0.0.1:8000/'
#
# class TestUserLogin(unittest.TestCase):
#
#     login_url = BASE_URL + "user/login/"
#     def test_login_success(self):
#         # Prepare the data for a successful login
#         payload = {
#             'email': 'ana@gmail.com',
#             'password': 'anand123@'
#         }
#         cookies = {
#             'csrftoken': 'PKazoo2gmzFQsTJARsaWZlJDt5WqBi3y'
#         }
#
#         # Send the POST request
#         response = requests.post(self.login_url, data=payload, cookies=cookies)
#
#         # Check response status code and content
#         self.assertEqual(response.status_code, 200)  # Assuming a successful login returns 200
#         self.assertIn('token', response.json())  # Assuming the response contains a token on success
#
#     def test_login_failure(self):
#         # Prepare invalid credentials for a failed login
#         payload = {
#             'email': 'invalid@gmail.com',
#             'password': 'wrongpassword'
#         }
#         cookies = {
#             'csrftoken': 'PKazoo2gmzFQsTJARsaWZlJDt5WqBi3y'
#         }
#
#         # Send the POST request
#         response = requests.post(self.login_url, data=payload, cookies=cookies)
#
#         # Check response status code and content
#         self.assertEqual(response.status_code, 401)  # Assuming a failed login returns 401
#         self.assertNotIn('token', response.json())  # No token should be returned on failure
#
# # if __name__ == '__main__':
# #     unittest.main()
#
#
# class TestUserRegistration(unittest.TestCase):
#     register_url = BASE_URL + 'user/register/'
#
#     def test_registration_success(self):
#         # Prepare the data for a successful registration
#         payload = {
#             'email': 'anand1@gmail.com',
#             'password': 'anand1@',
#             'first_name': 'anand1'
#         }
#         cookies = {
#             'csrftoken': 'PKazoo2gmzFQsTJARsaWZlJDt5WqBi3y'
#         }
#
#         # Send the POST request
#         response = requests.post(self.register_url, data=payload, cookies=cookies)
#
#         # Check response status code and content
#         self.assertEqual(response.status_code, 201)  # Assuming a successful registration returns 201
#         self.assertIn('message', response.json())  # Assuming the response contains a success message
#
#     def test_registration_failure_duplicate_email(self):
#         # Prepare data with an existing email for a failed registration
#         payload = {
#             'email': 'abcc@gmail.com',  # Assuming this email is already registered
#             'password': 'anand1@',
#             'first_name': 'anand1'
#         }
#         cookies = {
#             'csrftoken': 'PKazoo2gmzFQsTJARsaWZlJDt5WqBi3y'
#         }
#
#         # Send the POST request
#         response = requests.post(self.register_url, data=payload, cookies=cookies)
#
#         # Check response status code and content
#         self.assertEqual(response.status_code, 400)  # Assuming a duplicate email returns 400
#         self.assertIn('error', response.json())  # Assuming the response contains an error message
#
#     def test_registration_failure_missing_fields(self):
#         # Prepare data missing required fields for a failed registration
#         payload = {
#             'email': 'new_email@gmail.com',
#             # Missing password and first_name
#         }
#         cookies = {
#             'csrftoken': 'PKazoo2gmzFQsTJARsaWZlJDt5WqBi3y'
#         }
#
#         # Send the POST request
#         response = requests.post(self.register_url, data=payload, cookies=cookies)
#
#         # Check response status code and content
#         self.assertEqual(response.status_code, 400)  # Assuming a missing fields returns 400
#         self.assertIn('error', response.json())  # Assuming the response contains an error message
#
#
# if __name__ == '__main__':
#     unittest.main()

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Adjust the URL name as needed
        self.login_url = reverse('login')        # Adjust the URL name as needed

    def test_registration_success(self):
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass@123',
            'first_name': 'Test'
        }
        response = self.client.post(self.register_url, payload)

        # Check for successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)  # Assuming a success message is returned

    def test_registration_failure_duplicate_email(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass@123'
        )
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass@123',
            'first_name': 'Test'
        }
        response = self.client.post(self.register_url, payload)

        # Check for failure due to duplicate email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Adjust based on actual error response

    def test_registration_failure_missing_fields(self):
        payload = {
            'email': 'new_email@gmail.com',
            # Missing password and first_name
        }
        response = self.client.post(self.register_url, payload)

        # Check for failure due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for specific error details in the response
        self.assertIn('password', response.data)  # Check that 'password' is in the response

        # Check that the 'password' field contains the required message
        self.assertEqual(response.data['password'][0].code, 'required')
        # self.assertEqual(response.data['first_name'][0].code, 'required')

    def test_login_success(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass@123'
        )
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass@123'
        }
        response = self.client.post(self.login_url, payload)

        # Check for successful login
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming a token is returned on success

    def test_login_failure_invalid_credentials(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass@123'
        )
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, payload)

        # Check for failure due to invalid credentials
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)  # Adjust based on actual error response

# To run the tests, use the following command in your terminal:
# python manage.py test <your_app_name>
