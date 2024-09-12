from django.shortcuts import render
from django.db.models import Q

from .models import *
from .serializers import *

from rest_framework import generics
from rest_framework.exceptions import NotFound


class PaperList(generics.ListCreateAPIView):
    serializer_class = PapersListSerializer

    def get_queryset(self):
        return Papers.objects.all()



class PaperDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PapersListSerializer
    lookup_field = 'name'

    def get_object(self):
        name = self.kwargs.get('name').replace('_', ' ')
        # Case-insensitive lookup for the paper name
        obj = Papers.objects.filter(name__iexact=name).first()
        if obj is None:
            raise NotFound(detail="Paper not found")
        return obj


class TypeList(generics.ListCreateAPIView):
    serializer_class = TypeListSerializer

    def get_queryset(self):
        return Type.objects.all()


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TypeListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return Type.objects.filter(name=name)


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return Category.objects.filter(name=name)


class SubCategoryList(generics.ListCreateAPIView):
    serializer_class = SubCategoryListSerializer

    def get_queryset(self):
        return SubCategory.objects.all()


class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategoryListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name').replace('_', ' ')
        return SubCategory.objects.filter(name=name)
    

# views.py
from django.core.mail import send_mail
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt  # Disable CSRF protection for this view
def send_download_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paper_names = data.get('paper_names', [])
            download_links = data.get('download_links', [])
            prices = data.get('prices', [])
            currency_code = data.get('currency_code', '')
            user_email = data.get('user_email')
            from_email = settings.DEFAULT_FROM_EMAIL
            user = data.get('user')  # Retrieve user's info from the request

            # Construct the HTML email message
            subject = 'Your Purchased Papers Download Links'
            message = f"""
<html>
<head>
    <style>
        /* Your CSS styles */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            Iwemi Research
        </div>
        <div class="content">
            <h1>Thank you for your purchase!</h1>
            <p>Dear {user.get('name')} {user.get('last_name')},</p>
            <p>Thank you for purchasing from our store. Below are the details of your order:</p>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>Download Link</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'''
                        <tr>
                            <td>{paper_name}</td>
                            <td>{currency_code} {price}</td>
                            <td><a href="{download_link}">Download</a></td>
                        </tr>
                        ''' for paper_name, price, download_link in zip(paper_names, prices, download_links))}
                    </tbody>
                </table>
            </div>
            <p>If you have any questions or need further assistance, feel free to contact our support team.</p>
            <p>Best regards,</p>
            <p><strong>Iwemi Research Team</strong></p>
        </div>
        <div class="footer">
            <p>This email was sent to {user_email} because you made a purchase on our website. If you did not make this purchase, please contact our support team immediately.</p>
        </div>
    </div>
</body>
</html>
            """

            send_mail(
                subject,
                '',  # No plain text message needed when using HTML email
                from_email,
                [user_email],  # Send to the user's email
                fail_silently=False,
                html_message=message,  # Send HTML message
            )

            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
