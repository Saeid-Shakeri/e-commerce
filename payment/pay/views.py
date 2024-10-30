import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer


class PaymentView(APIView):

    @swagger_auto_schema(
            request_body=PaymentSerializer,
            operation_id="process_simulation",
            # operation_summary="Change user Email",
            # operation_description="This endpoint allows you to ..."
    )
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        with connections['external_db'].cursor() as cursor:
            cursor.execute("SELECT id, status FROM Order WHERE id = %s", [order_id]) # order = ExternalOrder.objects.using('external_db').get(id=order_id)
            order = cursor.fetchone()
            
            if not order:
                return Response({'error': 'Order not found in external database'}, status=status.HTTP_404_NOT_FOUND)
            
            if random.random() < 0.8:
                new_status = 'paid'
                result = 'success'
            else:
                new_status = 'failed'
                result = 'failed'
            
            cursor.execute("UPDATE Order SET status = %s WHERE id = %s", [new_status, order_id])

        return Response({'status': result}, status=status.HTTP_200_OK)
