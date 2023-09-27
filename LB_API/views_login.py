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
import time
from django.http import JsonResponse

# Obtiene la marca de tiempo actual en segundos
marca_de_tiempo = int(time.time())


@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        data = request.data
        try:
            usuario = User.objects.get(email=data['email'])
            if usuario:
                return Response({'error': 'el usuario ya existe'})
            else:
                dir = Direction.objects.get(id = data['numero'])
                if dir:
                    return Response({'error': 'No se pudo agregar la direccion intentelo mas tarde'})      
        except:
            dir = Direction.objects.create(
                id = marca_de_tiempo + data['numero'],
                nombre=data['nombre_dir'],
                calle=data['calle'],
                numero=data['numero'],
                commune=Commune.objects.get(id = data['id_com'])
            )
            user = User.objects.create(
                id = dir.id - 100,
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
            return JsonResponse({'success':'El usuario ah sido creado','UserData': userSerial})
            
            
@api_view(['POST'])
def loginUser(request):
    if request.method == 'POST':
        try:
            pass1 = make_password(request['password'])
            user = User.objects.get(email=request['email'], password=pass1)
            if user:
                user1= authenticate(username=request['email'], password=pass1)
                token = Token.objects.get_or_create(user=user)
                if token:
                    login(request, user1)
                    serial = userSerializer(user, many=False)
                    return Response(serial.data)
                else:
                    return Response({'error':'Usuario no autorizado'})
            else:
                return Response({'error':'El usuario no existe'})
        except:
            msj = 'el usuario no existe o contraseña incorrecta'
            return  JsonResponse({'error' : msj})



    
@api_view(['PUT'])
def editUser(request, id):
    try:
        user1 = User.objects.get(id=id)
        AdminUser.objects.get(username=user1.email)
        userSerial = userSerializer(user1, data=request.data)
        if user1:
            token = Token.objects.get(user=user1)
            if token:
                if userSerial.is_valid():
                    userSerial.save()
                    return Response({'userData':userSerial})
                else:
                    return Response(userSerial.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'El Usuario no esta autenticado'})
        else:
            return Response({'error':'El usuario no existe'})
    except:
        return Response({'error':'Ha ocurrido un error'})


