from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status 
from .models import *
from rest_framework import status
from rest_framework.test import APITestCase


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(category.description, 'All kinds of electronic products')


class ApiCategoryListTest(APITestCase):
    def test_get_categories(self):
        categories = [
            Category(name="Electronics", description="All kinds of electronic products"),
            Category(name="Clothes", description="All kinds of Fashion Clothes")
        ]
        Category.objects.bulk_create(categories)
        url = '/categories/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductModelTest(TestCase):

    def test_product_creation(self):
        category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
        product = Product.objects.create(
            name="Laptop", description="A powerful laptop", price=1000, quantity=50, category=category
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.category, category)
        self.assertTrue(product.in_stock)

    def test_product_quantity_update(self):
        category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
        product = Product.objects.create(
            name="Laptop", description="A powerful laptop", price=1000, quantity=50, category=category
        )
        product.quantity = 30
        product.save()
        self.assertEqual(product.quantity, 30)

    def test_product_price_update(self):
            category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
            product = Product.objects.create(
                name="Laptop", description="A powerful laptop", price=1000, quantity=50, category=category
            )
            product.price = 3000
            product.save()
            self.assertEqual(product.price, 3000)

    def test_product_in_stock_update(self):
            category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
            product = Product.objects.create(
                name="Laptop", description="A powerful laptop", price=1000, quantity=50, category=category
            )
            product.in_stock = not product.in_stock
            product.save()
            self.assertEqual(product.in_stock, False)
            product.in_stock = not product.in_stock
            product.save()
            self.assertEqual(product.in_stock, True)


class APIProductListTest(APITestCase):

    def test_get_product(self):
        category = Category.objects.create(name="Electronics", description="All kinds of electronic products")
        products = [
            Product(name="laptop",description="a powerful laptop",price=10,quantity=5,category=category)
        ]
        Product.objects.bulk_create(products)
        url = '/products/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

