
from rest_framework import viewsets
from .serializer import CommuneSerializer
from .models import Commune
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view(['GET']) 
def getCommunes(request):
    comune = Commune.objects.all()
    comunasSerial = CommuneSerializer(comune, many=True)
    return JsonResponse({'dataCommune': comunasSerial})
