from django.db import models


class Order(models.Model):
    user_id = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[
        ("incomplete", "Incomplete"), ('paid', 'Paid'), ('failed', 'Failed'), ('canceled', 'Cancelled')]
        , default='incomplete')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - User {self.user_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItem {self.id} - Order {self.order.id} - Product {self.product_id}"
