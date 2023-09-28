from rest_framework import viewsets
from .serializer import BookSerializer, BookCategorySerializer, CommentsSerializer
from .models import Book, Comments, BookCategory, User, BookState
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from rest_framework import status

class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all() 
    
class BookCategoryView(viewsets.ModelViewSet):
    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all() 
    
class CommentsView(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

@api_view(['POST'])
def book_create(request):
    if request.method == 'POST':
        data = request.data
        try:
            Book.objects.get(name=data['name'])
            return Response({'error': 'El libro ya existe'})
        except Book.DoesNotExist:
            book = Book.objects.create(
                name=data['name'],
                price=data['price'],
                description=data['description'],
                author=data['author'],
                book_img=data['book_img'],
                seller=User.objects.get(id=data['seller']),
                book_state=BookState.objects.get(id=data['book_state']),
                valoration=data['valoration'],
                book_category=BookCategory.objects.get(id=data['book_category'])
            )
            book_serialized = BookSerializer(book, many=False)
            return Response({'BookData': book_serialized.data})
        except Exception as e:
            return Response({'error': str(e)})


@api_view(['PUT'])
def book_update(request, pk):
    try:
        # Obtén el libro existente por su clave primaria (ID)
        book = Book.objects.get(pk=pk)
        # Actualiza los campos del libro con los datos proporcionados en la solicitud
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
@api_view(['DELETE'])
def book_delete(request):
        __name__ = list(book_delete.objects.filter(request=request).values())
        if len(__name__) > 0:
            __name__.objects.filter(request=request).delete()
            datos = {'message': "Eliminado"}
        else:
            datos = {'message': "El libro fue Eliminado..."}
        return Response(datos) 
    
@api_view(['GET'])    
def book_get(request):
        if (request > 0):
            __name__= list(book_get.objects.filter(request=request).values())
            if len(__name__) > 0:
                book_get = __name__[0]
                datos = {'message': "Success", 'Libros': book_get}
            else:
                datos = {'message': "Book not found..."}
            return Response(datos)
        else:
            __name__ = list(book_get.objects.values())
            if len(__name__)) > 0:
                datos = {'message': "Success", 'companies': __name__}
            else:
                datos = {'message': "Book not found..."}
            return Response(datos)
