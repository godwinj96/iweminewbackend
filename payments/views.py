import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(APIView):
    def post(self, request):
        try:
            amount = int(request.data.get('amount', 0))
            currency = request.data.get('currency', 'ngn')
            success_url = request.data.get('success_url', 'http://localhost:5173/success')
            cancel_url = request.data.get('cancel_url', 'http://localhost:5173/cancel')
            name = request.data.get('productname', 'Research paper')
            order_id = request.data.get('order_id')  # Get the order ID from request

            # Create a Stripe Checkout session with metadata (order ID)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {'name': name},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={'order_id': order_id}  # Attach order_id as metadata
            )
            
            return Response({
                'session': session,
                'id': session.id,
                'publicKey': settings.STRIPE_PUBLIC_KEY
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from useraccount.models import Orders  # Import your Orders model

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # Store your webhook secret in Django settings

        try:
            # Verify the webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Payment was successful
            handle_payment_success(session)  # Call a function to update order

        return HttpResponse(status=200)


def handle_payment_success(session):
    order_id = session['metadata']['order_id']  # You can pass order_id via metadata when creating session
    try:
        order = Orders.objects.get(id=order_id)
        order.status = 'paid'
        order.save()
    except Orders.DoesNotExist:
        print(f"Order {order_id} does not exist")


