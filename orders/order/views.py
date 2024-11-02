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


class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_id = request.data['order_id']
            try:
                order = Order.objects.get(id=order_id,user_id=request.user)
                if order.status != 'incomplete':
                    return Response('this order completed',status=400)

            except Exception as e:
                return Response(f'Error : {e} {order_id}',status=400)
            product_id = request.data['product_id']
            try:
                p = Product.objects.get(id=product_id,in_stock=True)
            except Exception as e:
                return Response(f'Error : product not found , or not in stock {product_id}',status=400)
            quantity = request.data['quantity']
            if p.quantity >= quantity:
                OrderItem.objects.create(order=order,product_id=p,
                        quantity=quantity,price=p.price)
                order.total_price += p.price * quantity
                order.save()
                return Response({'status':'added succesfully'},status=200)
            else :
               return Response({'error': 'Not enough in stock'},status=409)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)
