from .models import Book, User, Review, Forum, ForumUser
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

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def review_delete(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        user = User.objects.get(email=request.user.username)

        if user == review.user:
            review.delete()
            return Response({'message': 'Reseña eliminada con éxito'})
        else:
            return Response({'error': 'No tienes permiso para eliminar esta reseña.'}, status=status.HTTP_403_FORBIDDEN)
        
    except review.DoesNotExist:
        return Response({'error': 'la reseña no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_forum(request, pk):
    try:
        forum = Forum.objects.get(pk=pk)
        user = User.objects.get(email=request.user.username)

        if user == forum.user:
            forum.delete()
            return Response({'message': 'Foro eliminado con éxito'})
        else:
            return Response({'error': 'No tienes permiso para eliminar este foro.'}, status=status.HTTP_403_FORBIDDEN)
        
    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def leave_forum(request, forum_id):
    try:
        # Obtén el usuario autenticado
        user = User.objects.get(email=request.user.username)

        # Obtén el foro
        forum = Forum.objects.get(id=forum_id)

        # Verifica si el usuario es miembro del foro
        forum_user = ForumUser.objects.get(user=user, forum=forum)

        # Elimina la relación entre el usuario y el foro
        forum_user.delete()

        return Response({'message': 'Te has salido del foro exitosamente.'}, status=status.HTTP_200_OK)
    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except ForumUser.DoesNotExist:
        return Response({'error': 'No eres miembro de este foro.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)