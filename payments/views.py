import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(APIView):
    def post(self, request):
        try:
            # Get the necessary data
            amount = int(request.data.get('amount', 0))   # Amount in cents
            currency = request.data.get('currency', 'ngn')
            success_url = request.data.get('success_url', 'http://localhost:5173/success')
            cancel_url = request.data.get('cancel_url', 'http://localhost:5173/cancel')
            name = request.data.get('productname', 'Research paper')

            print(request.data)

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': currency,
                            'product_data': {
                                'name': name,
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )
            print(session)
            return Response({
                'session': session,
                'id': session.id,
                'publicKey': settings.STRIPE_PUBLIC_KEY
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
