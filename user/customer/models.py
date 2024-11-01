from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=14,null=True,blank=True)
    
    class Meta:
        db_table = "customers"

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        db_table = "categories"

    


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    class Meta:
        db_table = "products"



class Order(models.Model):
    user_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=[
        ("incomplete", "Incomplete"), ('paid', 'Paid'), ('failed', 'Failed'), ('canceled', 'Cancelled')]
        , default='incomplete')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    class Meta:
        db_table = "order_items"
