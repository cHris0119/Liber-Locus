from .serializer import userSerializer
from .models import User, UserRole, Role, Direction, Commune, Subscription
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as AdminUser

@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        data = request.data
        try:
            User.objects.get(email=data['email'])
            return Response({'error': 'el usuario ya existe'})
        except:
               
            dir = Direction.objects.create(
                nombre=data['nombre_dir'],
                calle=data['calle'],
                numero=data['numero'],
                commune=Commune.objects.get(id = data['id_com'])
            )
        
            User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password']),
                created_at=datetime.now(),
                direction=Direction.objects.get(id = dir.id),
                user_photo=data['photo_dir'],
                subscription=Subscription.objects.get(id = 1)
            )
            
            AdminUser.objects.create(username=data['email'], password=data['password'])
            
            
            
            
            
            
        
@api_view(['GET'])
def loginUser(request):
    try:
        user = User.objects.get(request['email'], request['password'])
        if user:
            serial = userSerializer(user, many=False)
            return Response(serial.data)
    except:
        msj = 'el usuario no existe o contraseña incorrecta'
        return  Response({'error' : msj})
    
    



