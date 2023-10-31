from .models import Book, User, Review, Forum, ForumUser, Discussion, Question
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_discussion(request, discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        user = User.objects.get(email=request.user.username)

        # Asegúrate de que el usuario actual sea el creador de la discusión
        if ForumUser.objects.filter(user=user, forum=discussion.forum_user.forum).exists():
            if user == discussion.forum_user.user:
                discussion.delete()
                return Response({'message': 'Discusión eliminada con éxito'})
            else:
                return Response({'error': 'No tienes permiso para eliminar esta discusión.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'El usuario no es miembro de este foro.'}, status=status.HTTP_403_FORBIDDEN)

    except Discussion.DoesNotExist:
        return Response({'error': 'La discusión no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_user_from_forum(request, forum_id, user_id):
    try:
        current_user = User.objects.get(email=request.user.username) # Usuario quien pide la eliminación
        forum = Forum.objects.get(id=forum_id) # ID actual del foro
        user_to_remove = User.objects.get(id=user_id) # Usuario quien será eliminado

        # Si el usuario que hace la petición no es del foro del foro, no puede hacer la acción
        if current_user != forum.user:
            return Response({'error': 'No tienes permiso para eliminar a este usuario del foro.'}, status=status.HTTP_403_FORBIDDEN)

        # Realiza la lógica para eliminar al usuario del foro
        forum_user_to_remove = ForumUser.objects.filter(user=user_to_remove, forum=forum)

        if forum_user_to_remove.exists():
            forum_user_to_remove.delete()
            return Response({'message': 'Usuario eliminado del foro exitosamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El usuario no es miembro de este foro.'}, status=status.HTTP_400_BAD_REQUEST)

    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def QuestionDelete(request, Q_id):
    try:
        user = User.objects.get(email = request.user.username)
        quest = Question.objects.get(id = Q_id)
        if quest:
            if quest.user == user:
                try:
                    quest.delete()
                    return Response({'msj':'la pregunta se ha eliminado exitosamente'}, status=status.HTTP_200_OK)
                except user.DoesNotExist:
                    return Response({'error':'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND) 
            else:
                return Response({'error':'El usuario no esta autorizado a eliminar esta pregunta'}, status=status.HTTP_401_UNAUTHORIZED)            
        else:
            return Response({'error':'La pregunta no existe'}, status=status.HTTP_404_NOT_FOUND)    
    except Exception as e:
         return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)