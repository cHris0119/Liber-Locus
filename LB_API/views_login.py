from .serializer import userSerializer
from .models import User, UserRole, Role, Direction, Commune, Subscription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as AdminUser
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token 

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
            user = User.objects.create(
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
            userSerial = userSerializer(user, many=False)
            return Response({'UserData': userSerial})
            
            
@api_view(['GET'])
def loginUser(request):
    try:
        user = User.objects.get(email=request['email'], password=request['password'])
        if user:
            user1= AdminUser.authenticate(username=request['email'], password=request['password'])
            token = Token.objects.get_or_create(user=user)
            if token:
                login(request, user1)
                serial = userSerializer(user, many=False)
                return Response(serial.data)
    except:
        msj = 'el usuario no existe o contraseña incorrecta'
        return  Response({'error' : msj})
    
    
@api_view(['PUT'])
def editUser(request, id):
    try:
        user1 = User.objects.get(id=id)
        AdminUser.objects.get(username=user1.email)
        if user1:
            token = Token.objects.get(user=user1)
            if token:
                pass
    except:
        return Response({'error':'Ha ocurrido un error'})


