from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Category, Product, Order, OrderItem


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
        self.assertEqual(customer.username, 'testuser')
        self.assertEqual(customer.email, 'testuser@example.com')
        self.assertTrue(customer.check_password('password123'))


class APICustomerRegisterTest(APITestCase):
    def test_create_customer(self):
        url = '/register/'
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')


# class ApiChangeEmailTest(APITestCase):
#     def setUp(self):
#         self.user = Customer.objects.create(username='user', password='password', email='admin@example.com')
#         url = '/token/'
#         data = { 'username': 'user', 'password': 'password' }
#         response = self.client.post(url, data, format='json')
#         print(response)
#         print(response.data)
#         self.token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

#     def test_change_email(self):
#         url = '/change-email/'
#         data = { 'email': 'fake@example.com' }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(self.user.email, 'fake@example.com')
