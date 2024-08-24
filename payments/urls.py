from django.urls import path
from .views import CreateStripeCheckoutSessionView

urlpatterns = [
    path('create-payment-intent/', CreateStripeCheckoutSessionView.as_view(), name='create-payment-intent'),
]