from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from .serializers import SendEmailSerializer
from .permissions import IsAdmin


class SendEmailView(APIView):
    permission_classes = (IsAdmin,)

    @swagger_auto_schema(
        request_body=SendEmailSerializer,
        operation_id="send_email",
    )
    def post(self, request, *args, **kwargs):
        user_email = request.data.get('email')
        if not user_email:
            return Response({'error': 'Email is required'}, status=400)

        send_mail(
            'Order Confirmation',
            'Your order has been placed successfully.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
        return Response({'succes': 'Email Sended Successfuly '})