from .serializer import userSerializer, TokenSerializer
from .models import User, UserRole, Role, Direction, Commune, Subscription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.models import User as AdminUser
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token 
import time
import re
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import base64
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile




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
                dir_user = User.objects.get(direction = dir)
                # if dir_user:
                #     return Response({'error': 'No se pudo agregar la dirección, inténtelo más tarde'}, status=status.HTTP_400_BAD_REQUEST)
            except Direction.DoesNotExist:
                if len(passw) > 8:
                    if validacionCE(data['password']):
                        if validacionMAYUS(data['password']):
                            if validacionNum(data['password']):
                                image_data = data['photo_dir']
                                if image_data.startswith("data:image"):
                                    try:
                                        image_data = image_data.split(",")[1]
                                        image_bytes = base64.b64decode(image_data)
                                        image = Image.open(BytesIO(image_bytes))
                                        user = User.objects.create(
                                            id=marca_de_tiempo,
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            email=data['email'],
                                            password=make_password(data['password']),
                                            created_at=datetime.now(),
                                            subscription=Subscription.objects.get(id=1)
                                        )

                                        user.user_photo.save(f"{user.email}.png", ContentFile(image_bytes), save=True)
                                        user.save()
                                
                                        if user:
                                            dir = Direction.objects.create(
                                            id=marca_de_tiempo,
                                            nombre=data['nombre_dir'],
                                            calle=data['calle'],
                                            numero=data['numero'],
                                            commune=Commune.objects.get(id=data['id_com']),
                                            user_id=user.id
                                            )
                                        
                                            AdminUser.objects.create(username=data['email'], password=make_password(data['password']))
                                            userSerial = userSerializer(user, many=False)
                                            return Response({'success': 'El usuario ha sido creado', 'UserData': userSerial.data}, status=status.HTTP_201_CREATED)
                                        else:
                                            return Response({'error': 'No se pudo crear la direccion'}, status=status.HTTP_400_BAD_REQUEST)
                                    except Exception as e:
                                        return Response({'error': 'Error al decodificar y guardar la imagen'}, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    return Response({'error': 'Los datos de la imagen no están en el formato correcto'}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({'error': 'La contraseña debe tener al menos un numero'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'error': 'La contraseña debe tener al menos una mayuscula'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': 'La contraseña debe tener al menos un caracter especial ej(!@#$)'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'La contraseña debe tener al menos 8 caracteres'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        data = request.data
        user = authenticate(username=data['email'], password=data['password'])

        if user is not None:
            user1 = User.objects.get(email=data['email'])
            user_profile = User.objects.get(email=data['email'])  # Obtén el perfil del usuario por su correo electrónico
            token, created = Token.objects.get_or_create(user=user)
            serialToken = TokenSerializer(token)
            serialUser = userSerializer(user1,many=False)
            user_data = {
                'id': serialUser.data['id'],
                'first_name': serialUser.data['first_name'],
                'last_name': serialUser.data['last_name'],
                'user_photo': serialUser.data['user_photo']
            }
            # Obtén la dirección del usuario y agrégala a los datos de usuario
            user_direction = Direction.objects.get(id=user_profile.id)
            direction_data = {
                'nombre': user_direction.nombre,
                'calle': user_direction.calle,
                'numero': user_direction.numero,
                'commune': user_direction.commune.id  # Ajusta esto según tus necesidades
            }
            user_data['direction'] = direction_data

            login(request, user)
            return Response({'msj': 'Autenticación exitosa', 'token': serialToken.data['key'], 'userData': user_data}, status=status.HTTP_200_OK)
        else:
            # Usuario o contraseña incorrecta
            return Response({'msj': 'El usuario no existe o la contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@csrf_exempt
def logout(request, id):
    if request.method == 'POST':
        user = User.objects.get(id = id)
        user1 = AdminUser.objects.get(username=user.email)
        if user:
            token = Token.objects.get(user = user1)
            if token:
                token.delete()
                return Response({'msj': 'Usuario deslogeado exitosamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'msj': 'No Autorizado para hacer esta acciion'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'msj': 'El usuario no existe o la contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
        





