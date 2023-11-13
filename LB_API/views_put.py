from .serializer import BookSerializer, ForumCategorySerializer, EditForumSerializer, EditReviewSerializer, BookCategorySerializer , EditBooksSerializer, sellerSerializer, userSerializer, editDirectionSerializer, ReviewSerializer, ForumSerializer
from .models import Book, BookCategory, User, Direction, Review, Forum, ForumUser, ForumCategory
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response  
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as AdminUser
from rest_framework.authentication import TokenAuthentication
import base64
from .functions import get_image_format, base64_image
import os

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
    data = request.data
    try:
        usernow = User.objects.get(email = request.user.username)
        user1 = User.objects.get(id=id)
        if user1 == usernow:
            serialUser = userSerializer(user1, data=data, partial=True)
            if serialUser.is_valid():
                serialUser.save()
                return Response({'userData':serialUser.data}, status=status.HTTP_200_OK)
            else:
                return Response(serialUser.errors, status=status.HTTP_400_BAD_REQUEST)
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

        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'El libro no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if user != book.seller:
            return Response({'error': 'No tienes permiso para actualizar este libro.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EditBooksSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Personaliza la respuesta para incluir la información adicional
            book_data = {
                'id': serializer.data['id'],
                'name': serializer.data['name'],
                'price': serializer.data['price'],
                'description': serializer.data['description'],
                'author': serializer.data['author'],
                'created_at': serializer.data['created_at'],
                'seller': sellerSerializer(book.seller).data,
                'book_category': BookCategorySerializer(book.book_category).data,
                'book_img': base64_image('media/' + str(book.book_img)),
                'format': get_image_format('media/' + str(book.book_img))
            }

            return Response(book_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_update(request, pk):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        review = Review.objects.get(pk=pk)

        if review:
            if user == review.user:
                serializer = EditReviewSerializer(review, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()

                    # Personaliza la respuesta para incluir información adicional
                    response_data = [{
                        'id': serializer.data['id'],
                        'title': serializer.data['title'],
                        'created_at': review.created_at,
                        'valoration': serializer.data['valoration'],
                        'user': sellerSerializer(review.user).data,
                        'description': serializer.data['description'],
                        'review_img': base64_image(f'media/{review.review_img}'),
                        'format': get_image_format(f'media/{review.review_img}'),
                    }]

                    return Response(response_data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No tienes permiso para actualizar esta reseña.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'La reseña no existe.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_forum(request, pk):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        forum = Forum.objects.get(pk=pk)

        if forum:
            if user == forum.user:
                serializer = EditForumSerializer(forum, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()

                    # Personaliza la respuesta para incluir información adicional
                    response_data = {
                        'id': forum.id,
                        'name': forum.name,
                        'created_at': forum.created_at,
                        'forum_category': ForumCategorySerializer(ForumCategory.objects.get(id=forum.forum_category_id)).data['id'],
                        'user': sellerSerializer(forum.user).data,
                        'forum_img': base64_image(f'media/{forum.forum_img}'),
                        'format': get_image_format(f'media/{forum.forum_img}'),
                    }

                    return Response({'UpdatedForumData': response_data})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No tienes permiso para actualizar este foro.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)