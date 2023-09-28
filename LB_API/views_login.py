from .serializer import userSerializer, TokenSerializer
from .models import User, UserRole, Role, Direction, Commune, Subscription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.models import User as AdminUser
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token 
import time
import re
from django.contrib.auth.hashers import make_password, check_password


def validacionCE(passw):
    special_characters_pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\]'
    
    if re.search(special_characters_pattern, passw):
        return True
    else:
        return False
    
def validacionMAYUS(passw):
    mayus = r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]'
    
    if re.search(mayus, passw):
        return True
    else:
        return False
    
def validacionNum(passw):
    num = r'[1234567890]'
    
    if re.search(num, passw):
        return True
    else:
        return False

# Obtiene la marca de tiempo actual en segundos
marca_de_tiempo = int(time.time())



@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        data = request.data
        passw = data['password']
        try:
            User.objects.get(email=data['email'])
            return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            try:
                dir = Direction.objects.get(calle = data['calle'], numero = data['numero'])
                return Response({'error': 'No se pudo agregar la dirección, inténtelo más tarde'}, status=status.HTTP_400_BAD_REQUEST)
            except Direction.DoesNotExist:
                if len(passw) > 8:
                    if validacionCE(data['password']):
                        if validacionMAYUS(data['password']):
                            if validacionNum(data['password']):
                                dir = Direction.objects.create(
                                    id=marca_de_tiempo,
                                    nombre=data['nombre_dir'],
                                    calle=data['calle'],
                                    numero=data['numero'],
                                    commune=Commune.objects.get(id=data['id_com'])
                                )
                                
                                user = User.objects.create(
                                    id=marca_de_tiempo,
                                    first_name=data['first_name'],
                                    last_name=data['last_name'],
                                    email=data['email'],
                                    password=make_password(data['password']),
                                    created_at=datetime.now(),
                                    direction=Direction.objects.get(id=dir.id),
                                    user_photo=data['photo_dir'],
                                    subscription=Subscription.objects.get(id=1)
                                )
                                AdminUser.objects.create(username=data['email'], password=make_password(data['password']))
                                userSerial = userSerializer(user, many=False)
                                return Response({'success': 'El usuario ha sido creado', 'UserData': userSerial.data}, status=status.HTTP_201_CREATED)
                            else:
                                return Response({'error': 'La contraseña debe tener al menos un numero'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'error': 'La contraseña debe tener al menos una mayuscula'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': 'La contraseña debe tener al menos un caracter especial ej(!@#$)'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loginUser(request):
    if request.method == 'POST':
        data = request.data
        user = authenticate(username=data['email'], password=data['password'])

        if user is not None:
            user1 = User.objects.get(email=['email'])
            token, created = Token.objects.get_or_create(user=user)
            serialToken = TokenSerializer(token)
            serialUser = userSerializer(user1, fields=('id', 'first_name', 'last_name'),many=False)
            login(request, user)
            return Response({'msj': 'Autenticación exitosa', 'token': serialToken.data['key'], 'userData': serialUser.data}, status=status.HTTP_200_OK)
        else:
            # Usuario o contraseña incorrecta
            return Response({'msj': 'El usuario no existe o la contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)




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
                return Response({'error': 'El Usuario no está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


