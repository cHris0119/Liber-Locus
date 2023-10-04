from .models import Book, User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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
