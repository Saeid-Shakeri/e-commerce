from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Customer
from .serializers import (CustomerRegisterSerializer,
        ProfileSerializer, ChangePasswordSerializer, ChangeEmailSerializer)


class CustomerRegisterView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer


class ProfileView(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "Object partially updated successfully",
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_id="change_user_password",
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
            request_body=ChangeEmailSerializer,
            operation_id="change_user_email",
            # operation_summary="Change user Email",
            # operation_description="This endpoint allows you to ..."
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.email = serializer.data.get("email")
            user.save()
            return Response({"status": "email set"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

