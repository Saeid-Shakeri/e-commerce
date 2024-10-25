from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude =('password','groups',)
    # search_fields = ['username']
