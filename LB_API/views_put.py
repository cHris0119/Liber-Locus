from .serializer import BookSerializer,  editBooksSerializer, editUserSerializer, editDirectionSerializer
from .models import Book, BookCategory, User, Direction
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response  
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as AdminUser
from rest_framework.authentication import TokenAuthentication

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def editDirection(request, id):
    if request.method == 'PUT':
        data = request.data
        try:
            data_dir = {
                'nombre' :data['nombre'],
                'calle' : data['calle'],
                'numero': data['numero'],
                'commune': data['id_com']
            }
            direction = Direction.objects.get(user_id=id)
            dirSerial = editDirectionSerializer(direction, data=data_dir, partial=True)
            if dirSerial.is_valid():
                dirSerial.save()
                return Response({'dirData': dirSerial.data}, status=status.HTTP_200_OK)
            else:
                return Response(dirSerial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Direction.DoesNotExist:
            return Response({'error': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editUser(request, id):
    try:
        user1 = User.objects.get(id=id)
        user = AdminUser.objects.get(username=user1.email)
        userSerial = editUserSerializer(user1, data=request.data)
        if user1:
            if userSerial.is_valid():
                userSerial.save()
                return Response({'userData':userSerial.data}, status=status.HTTP_200_OK)
            else:
                return Response(userSerial.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        book = Book.objects.get(pk=pk)
        book.book_category = BookCategory.objects.get(id = data['book_category'])
        bookSerial = editBooksSerializer(book, data=data)
        if book:
            if user == book.seller:
                bookSerial = BookSerializer(book, data=data, partial=True)        
                if bookSerial.is_valid():
                    bookSerial.save()
                    return Response(bookSerial.data)
                else:
                    return Response(bookSerial.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No tienes permiso para actualizar este libro.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'El libro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except BookCategory.DoesNotExist:
        return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
