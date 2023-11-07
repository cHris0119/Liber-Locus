from .serializer import userSerializer, TokenSerializer
from .models import User, UserRole, Role, Direction, Commune, Subscription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.contrib.auth.models import User as AdminUser
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token 
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from django.core.files.base import ContentFile
from .views_post import send_email
from .functions import validacionCE, validacionMAYUS, validacionNum, int_id, get_image_format
marca_de_tiempo = int_id()



@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        data = request.data
        passw = data['password']
        try:
            User.objects.get(email=data['email'])
            return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            if len(passw) > 8 & validacionCE(data['password']) & validacionMAYUS(data['password']) & validacionNum(data['password']):
                image_data = data['photo_dir']
                try:
                    print(1)
                    user = User.objects.create(
                        id=marca_de_tiempo,
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        email=data['email'],
                        password=make_password(data['password']),
                        created_at=datetime.now(),
                        subscription=Subscription.objects.get(id=1),
                        is_active=False,
                        confirm_key=None,
                        user_photo=None
                    )
                    print(2)
                    if image_data:
                        if image_data.startswith("data:image"):
                            image_data = image_data.split(",")[1]
                            image_bytes = base64.b64decode(image_data)
                            user.user_photo.save(f"{user.email}.png", ContentFile(image_bytes), save=True)
                            user.save()
                            print(3)
                                
                    if user:
                        dir = Direction.objects.create(
                            id=marca_de_tiempo,
                            nombre=data['nombre_dir'],
                            calle=data['calle'],
                            numero=data['numero'],
                            commune=Commune.objects.get(id=data['id_com']),
                            user=user
                        )
                        print(4)
                        send_email(user.email)
                        AdminUser.objects.create(username=data['email'], password=make_password(data['password']))
                        userSerial = userSerializer(user, many=False)
                        return Response({'success': 'El usuario ha sido creado', 'UserData': userSerial.data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'error': 'No se pudo crear la direccion'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print(str(e))
                    return Response({'error': 'Error al crear al usuario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'La contraseña no tiene el formato correcto'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return  Response({'error': 'Metodo no permitido'}, status=status.HTTP_400_BAD_REQUEST)
                    

@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        try:
            data = request.data
            user1 = User.objects.get(email = data['email'])
            if user1 is not None:
                user = authenticate(username=data['email'], password=data['password'])
                if user1.is_active:
                    image_base64 = None
                    format = None
                    token, created = Token.objects.get_or_create(user=user)
                    serialToken = TokenSerializer(token)
                    serialUser = userSerializer(user1,many=False)
                    img_path = 'media/' + str(user1.user_photo)
                    if user1.user_photo:
                        if os.path.exists(img_path):
                            with open(img_path, 'rb') as image_file:
                                image_data = image_file.read()
                                image_base64 = base64.b64encode(image_data)
                                format = get_image_format(img_path)
                    user_data = {
                        'id': serialUser.data['id'],
                        'first_name': serialUser.data['first_name'],
                        'last_name': serialUser.data['last_name'],
                        'user_photo': image_base64,
                        'format' : format
                    }
                    user_direction = Direction.objects.get(id=user1.id)
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
                    return Response({'Error':'Debes activar tu cuenta para poder ingresar, Porfavor verifica tu correo'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msj': 'El usuario o la contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
           return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except user1.DoesNotExist:
            return Response({'msj': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        

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
        





