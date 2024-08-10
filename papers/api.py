# from django.http import JsonResponse

# from rest_framework.decorators import api_view, authentication_classes, permission_classes

# from .models import Papers
# from .serializers import PapersListSerializer

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# def papers_list(request):
#     papers = Papers.objects.all()
#     serializer = PapersListSerializer(papers, many=True)

#     return JsonResponse({
#         'data': serializer.data
#     })