from .serializer import userSerializer
from .models import User, UserRole, Role, Direction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

@api_view(['POST'])
def registerUser(request):
    Direction.objects.create(
        
    )
    
    User.objects.create(
        first_name=request['first_name'],
        last_name=request['last_name'],
        email=request['email'],
        password=request['password'],
        created_at=datetime.now()
        direction=a,
        user_photo=a,
        subscription=
        
    )
        
        
@api_view(['GET'])
def loginUser(request, data):
    user = User.objects.get(id = data)
    
    serial = userSerializer(user, many=False)
    return Response(serial.data)



