from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import *
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
            return Response({"status": "email set"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login (req):
    if req.method == "GET":
        return render(req, 'signup_login.html',{})
    if req.method == "POST":
        context = {}
        context['categories'] = Category.objects.all()
        context ['products'] = Product.objects.all()
        return render(req, 'index.html',context)


def index(req):
    if req.method == "GET":
        context = {}
        context['categories'] = Category.objects.all()
        context ['products'] = Product.objects.all()
        return render(req, 'index.html',context)

# def products(req):
#     context = {}
#     context ['products'] = Product.objects.all()
#     return render(req, 'product.html',context)


# def categories(req):
#     context = {}
#     context ['categories'] = Category.objects.all()
#     return render(req, 'index.html',context)


def product(req, pk):
    context = {}
    context["product"] = Product.objects.filter(id=pk)
    return render(req, 'product.html',context)

def dashboard(request):
    if request.method == 'GET':
        context ={}
        context["user"] = request.user
        context["order"] = Order.objects.filter(user_id=request.user.id)
        print(context["order"])
        return render(request, "dashboard.html", context)

def edit_profile(request):
   
    user = request.user

    if request.method == 'GET':
        return render(request, 'edit_profile.html', {'user':user})

    if request.method == 'POST':
        try: 
            username = (request.POST.get('username')).strip()
            if username == '':
                message = ' نام کاربری نمیتواند خالی باشد.'
                return render(request,'edit_profile.html',{'message':message}) 
            u = User.objects.filter(username=username)
            for i in u :
                if username == i.username:
                    message = 'این نام کاربری موجود است لطفا یک نام دیگر را امتحان کنید.'
                    return render(request,'edit_profile.html',{'message':message}) 
            else :
                user.username = username
            if user.first_name != (request.POST.get("first_name")).strip():
                user.first_name = (request.POST.get("first_name")).strip()
            if user.last_name != (request.POST.get("last_name")).strip():
                user.last_name = (request.POST.get("last_name")).strip()
            if user.phone !=  (request.POST.get("phone")).strip():
                user.phone = (request.POST.get("phone")).strip()
            if user.email !=  (request.POST.get("email")).strip():
                if (request.POST.get("email")).strip() == '':
                    message = 'ایمیل نمیتواند خالی باشد.'
                    return render(request,'edit_profile.html',{'message':message}) 
                user.email = (request.POST.get("email")).strip()
            user.save()
            return redirect('dashboard')  
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'edit_profile view: {str(e)}')
            return render(request,'edit_profile.html',{'message':message,'user':request.user.id})



def change_password(request): 

    message = '' 
    if request.method == 'GET':
        return render(request, 'change_password.html', {})


    elif request.method == 'POST':
        try:
            oldpassword = (request.POST.get('oldpassword')).strip()
            user = request.user
            if  not user.check_password(oldpassword) :
                message = 'رمز قبلی را اشتباه نوشته اید. دوباره تلاش کنید. '
                return render(request,'change_password.html',{'message':message})
            password1 = (request.POST.get('password1')).strip()
            if len(str(password1)) < 8:
                message = 'رمز عبور نباید کمتر از 8 کاراکتر باشد. یک رمز دیگر بسازید.'
                return render(request,'change_password.html',{'message':message})
            password2 = (request.POST.get('password2')).strip()
            if password1 != password2 :
                message = 'رمز عبور جدید مطابقت ندارد دوباره تلاش کنید.'
                return render(request,'change_password.html',{'message':message})
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            message = 'A problem occurred. please try again later'
            logger.warning(f'change_password view: {str(e)}')
            return render(request,'change_password.html',{'message':message,'user':request.user.id})



def resetpass(request):
    pass


def message(request):
    context = {}
    context["message"] = Message.objects.filter(user=request.user).order_by('-date')
    return render(request,'messages.html', context)


def support(request):
    if request.method == "GET":
        context = {}
        l = []
        cat = cat_choices
        for c in cat:
            ca = c[1]
            l.append(ca)
        context['cat'] = l
        return render(request,'support.html', context)

    if request.method == "POST":
        cat = request.POST.get('cat')
        for c in cat_choices:
            if c[1] == cat:
                cat = c[0]
                break

        title = (request.POST.get('title')).strip()
        context = (request.POST.get('message')).strip()
        Message.objects.create(user=request.user,category=cat,context=context,title=title)

        return redirect('dashboard')

def logout(req):
    pass