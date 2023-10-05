
from .serializer import BookSerializer, ReviewSerializer
from .models import Book, BookCategory, User, Review
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
marca_de_tiempo = int(time.time())
from django.contrib.auth.models import User as AdminUser
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
                id=marca_de_tiempo,
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
            review = Review.objects.create(
            id = marca_de_tiempo,
            title = data['title'],
            created_at = datetime.now(),
            description = data['description'],
            valoration = data['valoration'],
            updated_at = datetime.now(),
            review_img = data['review_img'],
            user = User.objects.get(email = request.user.username))
            
            reviewSerial = ReviewSerializer(review, many=False)
            return Response({'reviewData': reviewSerial.data}) 
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)