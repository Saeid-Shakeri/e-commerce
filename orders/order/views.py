from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem, Product
from .permissions import IsAdmin
from .serializers import (OrderSerializer, OrderItemSerializer, AddToCartSerializer, 
    OrderCrateSerializer)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdmin,)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)


class OrderCreateView(APIView):
    serializer_class = OrderCrateSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        order = Order.objects.create(user_id=request.user)
        return Response({'result':'new order created succesfully', 'new_order_id':{order.id}})
