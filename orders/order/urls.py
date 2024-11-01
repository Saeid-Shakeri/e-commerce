from django.urls import path
from .views import (OrderListCreateView, OrderDetailView, AddToCartView,
     UserOrderListView, OrderCreateView)

urlpatterns = [

    # list and create for admin
    path('orders-admin/', OrderListCreateView.as_view(), name='order-list-create'),

    # add an item to cart
    path('orders/add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),

    # user orders list
    path('user-orders/', UserOrderListView.as_view(), name='user-order-list'),

    # user an order detail
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # create new order 
    path('new-order/', OrderCreateView.as_view(), name='create-new-order'),

]
