
from .serializer import BookSerializer, ReviewSerializer, ReviewLikeSerializer, ForumSerializer
from .models import Book, BookCategory, User, Review, ReviewLike, Forum, ForumCategory, ForumUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from django.contrib.auth.models import User as AdminUser
from django.utils import timezone


def int_id():
    # Obtener el tiempo actual en segundos desde la época (timestamp)
    timestamp = int(time.time())
    # Formatear el timestamp como DDMMSS
    formatted_time = time.strftime("%d%H%m%S", time.localtime(timestamp))
    # Convertir la cadena formateada a un número entero
    return int(formatted_time)



# Creacion de libros

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    if request.method == 'POST':
        data = request.data
        # Obtiene la marca de tiempo actual en segundos
        
        try:
            # Obtén el vendedor a partir del correo electrónico del usuario autenticado
            user_email = request.user.username
            seller = User.objects.get(email=user_email)

        except User.DoesNotExist:
            return Response({'error': 'El vendedor no existe'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            # Configura el valor predeterminado para BOOK_STATE_id
            book_state_id = 2  # Valor predeterminado deseado
            book_category = BookCategory.objects.get(id=data['book_category'])
                
            book = Book.objects.create(
                id=int_id(),
                name=data['name'],
                price=data['price'],
                description=data['description'],
                author=data['author'],
                book_img=data['book_img'],
                seller=seller,
                book_state_id=book_state_id,  # Establece el valor predeterminado
                book_category=book_category,
                created_at=datetime.now()
                )
            book_serialized = BookSerializer(book, many=False)
            
            return Response({'BookData': book_serialized.data})
        except BookCategory.DoesNotExist:
            return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])        
@permission_classes([IsAuthenticated])
def review_create(request):
    if request.method == 'POST':
        data = request.data
        try:
            usuario = User.objects.get(email = request.user.username)
            reviewUser = Review.objects.get(title = data['title'], user = usuario)
            if reviewUser:
                return Response({'error': 'Ya existe esa Reseña'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            try:
                review = Review.objects.create(
                id = int_id(),
                title = data['title'],
                created_at = datetime.now(),
                description = data['description'],
                valoration = data['valoration'],
                updated_at = datetime.now(),
                review_img = data['review_img'],
                user = usuario)
            
                reviewSerial = ReviewSerializer(review, many=False)
                return Response({'reviewData': reviewSerial.data})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])        
@permission_classes([IsAuthenticated])        
def like_a_post(request, id):
    if request.method == 'POST':
        user = User.objects.get(email = request.user.username)
        review = Review.objects.get(id = id)
        if user:
            try:
                reviewLike = ReviewLike.objects.create(
                    id = int_id(),
                    user = user,
                    review = review   
                )
                RSerial = ReviewLikeSerializer(reviewLike, many=False)
                return Response(RSerial.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_forum(request):
    if request.method == 'POST':
        data = request.data

        try:
            # Obtén el usuario autenticado
            user = User.objects.get(email=request.user.username)

        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Configura el valor predeterminado para FORUM_CATEGORY_id
            forum_category = ForumCategory.objects.get(id=data['forum_category'])

            forum = Forum.objects.create(
                id=int_id(),
                name=data['name'],
                created_at=datetime.now(),
                forum_img=data.get('forum_img', ''),
                forum_category=forum_category,
                user=user  # Asigna al usuario que creó el foro
            )

            forum_serialized = ForumSerializer(forum, many=False)

            return Response({'ForumData': forum_serialized.data})
        except ForumCategory.DoesNotExist:
            return Response({'error': 'La categoría del foro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_forum(request, id):
    if request.method == 'POST':
        user = User.objects.get(email=request.user.username)
        forum = Forum.objects.get(id=id)
        if user:
            # Verifica si el usuario ya es miembro del foro
            if ForumUser.objects.filter(user=user, forum=forum).exists():
                return Response({'message': 'Ya eres miembro de este foro.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                forum_user = ForumUser.objects.create(
                    id=int_id(),
                    user=user,
                    forum=forum
                )
                return Response({'message': 'Te has unido al foro exitosamente.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)