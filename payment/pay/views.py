from random import random
# from requests import post
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer
from .models import Order, Product, OrderItem
from kafka import KafkaProducer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
            request_body=PaymentSerializer,
            operation_id="payment_simulation",
            # operation_summary="Change user Email",
            # operation_description="This endpoint allows you to ..."
    )
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # with connections['external_db'].cursor() as cursor:
        #     cursor.execute("SELECT id, status FROM orders WHERE id = %s", [order_id]) # order = ExternalOrder.objects.using('external_db').get(id=order_id)
        #     order = cursor.fetchone()

        try:
            order = Order.objects.get(id=order_id)
        except Exception:
            return Response({'error': 'Order not found in external database'}, status=status.HTTP_404_NOT_FOUND)
        
        if random() < 0.8:
            new_status = 'paid'
            result = 'success'
        else:
            new_status = 'failed'
            result = 'failed'
        # cursor.execute("UPDATE orders SET status = %s WHERE id = %s", [new_status, order_id])
        order.status = new_status
        order.save()
        if new_status == 'paid':
            order_items = OrderItem.objects.filter(order_id=order.id)
            for item in order_items:
                p = Product.objects.get(id=item.product_id.id)
                p.quantity -= item.quantity
                p.save()

        email_data = {
            'order_id': order_id,
            'status': new_status,
            'email': request.user.email
        }
        # requests.post('http://localhost:8000/send_email/', json=email_data)

        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send('payment_result', {'email_data': email_data})
        producer.flush()

        return Response({'status': result}, status=status.HTTP_200_OK)
