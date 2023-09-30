
from rest_framework import viewsets
from .serializer import CommuneSerializer, BookCategorySerializer
from .models import Commune, BookCategory
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view(['GET']) 
def getCommunes(request):
    comune = Commune.objects.all()
    comunasSerial = CommuneSerializer(comune, many=True)
    return Response(comunasSerial.data)

@api_view(['GET']) 
def getCategories(request):
    category = BookCategory.objects.all()
    categorySerial = BookCategorySerializer(category, many=True)
    return Response(categorySerial.data)
