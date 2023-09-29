from rest_framework import viewsets
from .serializer import BookSerializer, BookCategorySerializer, CommentsSerializer
from .models import Book, Comments, BookCategory, User, BookState
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    if request.method == 'POST':
        data = request.data
        # Obtiene la marca de tiempo actual en segundos
        marca_de_tiempo = int(time.time())
        try:
                seller = User.objects.get(id=data['seller'])
        except User.DoesNotExist:
            return Response({'error': 'El vendedor no existe'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            book_state = BookState.objects.get(id=data['book_state'])
            book_category = BookCategory.objects.get(id=data['book_category'])
                
            book = Book.objects.create(
                id=marca_de_tiempo,
                name=data['name'],
                price=data['price'],
                description=data['description'],
                author=data['author'],
                book_img=data['book_img'],
                seller=seller,
                book_state=book_state,
                valoration=data['valoration'],
                book_category=book_category
                )
            book_serialized = BookSerializer(book, many=False)
            return Response({'BookData': book_serialized.data})
        except BookCategory.DoesNotExist:
            return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except BookState.DoesNotExist:
            return Response({'error': 'El estado del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
         
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    try:
        data = request.data
        # Obtén el libro existente por su clave primaria (ID)
        book = Book.objects.get(pk=pk)
        book_state = BookState.objects.get(id=data['book_state'])
        book_category = BookCategory.objects.get(id=data['book_category'])
        # Verifica si el campo "id" está presente en la solicitud y es un entero válido
        if 'id' in request.data and isinstance(request.data['id'], int):
            book.id = request.data['id']

        # Verifica si el campo "seller" está presente en la solicitud y es un entero válido
        if 'seller' in request.data and isinstance(request.data['seller'], int):
            book.seller_id = request.data['seller']
        
          # Verifica si el usuario autenticado es el propietario del libro
        if request.user != book.seller:
            return Response({'error': 'No tienes permiso para actualizar este libro.'}, status=status.HTTP_403_FORBIDDEN)

        # Actualiza otros campos del libro con los datos proporcionados en la solicitud
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except BookCategory.DoesNotExist:
        return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except BookState.DoesNotExist:
        return Response({'error': 'El estado del libro no existe'}, status=status.HTTP_404_NOT_FOUND)    
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response({'message': 'Libro eliminado con éxito'})
    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
@api_view(['GET'])
def get_all_books(request):
    try:
        # Obtén todos los libros de la base de datos
        books = Book.objects.all()
        # Serializa los libros para convertirlos en datos JSON
        serializer = BookSerializer(books, many=True)
        # Devuelve la lista de libros en la respuesta
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

