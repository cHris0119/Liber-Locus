from rest_framework import viewsets
from .serializer import BookSerializer, BookCategorySerializer, CommentsSerializer, editBooksSerializer
from .models import Book, Comments, BookCategory, User, BookState
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from math import trunc
from datetime import datetime

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    if request.method == 'POST':
        data = request.data
        # Obtiene la marca de tiempo actual en segundos
        marca_de_tiempo = int(time.time())
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
            
         
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        book = Book.objects.get(pk=pk)
        book_category = BookCategory.objects.get(id=data['book_category'])
        bookSerial = editBooksSerializer(book, data=request.data)
        
        if 'id' in request.data and isinstance(request.data['id'], int):
            book.id = request.data['id']

        if user == book.seller:
            bookSerial = BookSerializer(book, data=request.data, partial=True)  
                    
            if bookSerial.is_valid():
                bookSerial.save()
                return Response(bookSerial.data)
            else:
                return Response(bookSerial.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No tienes permiso para actualizar este libro.'}, status=status.HTTP_403_FORBIDDEN)

    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except BookCategory.DoesNotExist:
        return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        user = User.objects.get(email=request.user.username)

        if user == book.seller:
            book.delete()
            return Response({'message': 'Libro eliminado con éxito'})
        else:
            return Response({'error': 'No tienes permiso para actualizar este libro.'}, status=status.HTTP_403_FORBIDDEN)
        
    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    try:
        books = Book.objects.all()
        serialized_books = BookSerializer(books, many=True)    
        return Response(serialized_books.data)
    except Exception as e:
        return Response({'error': f'Ha ocurrido un error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_books(request):
    try:
        # Obtén el usuario autenticado
        user = User.objects.get(email=request.user.username)

        # Obtén todos los libros creados por el usuario
        books = Book.objects.filter(seller=user)

        # Serializa los libros para convertirlos en datos JSON
        serializer = BookSerializer(books, many=True)

        # Devuelve la lista de libros en la respuesta
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'No se encontraron libros para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)