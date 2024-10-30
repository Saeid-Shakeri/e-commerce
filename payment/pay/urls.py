from django.urls import path
from .views import ProcessPaymentView

urlpatterns = [
    path('payment/', ProcessPaymentView.as_view(), name="process-payment"),
]
