
from rest_framework import viewsets
from .serializer import userSerializer
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


class userView(viewsets.ModelViewSet):
    serializer_class = userSerializer
    queryset = User.objects.all()
