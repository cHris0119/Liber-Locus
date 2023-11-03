import os
from .functions import get_image_format
from django_backend import settings
from .serializer import CommuneSerializer, BookCategorySerializer, ReviewSerializer, userSerializer, DirectionSerializer, BookSerializer, ReviewLikeSerializer, ForumSerializer, ForumCategorySerializer, ForumUserSerializer, FollowSerializer, FollowedSerializer, QuestionSerializer, DiscussionSerializer, sellerSerializer, CommentsSerializer, AnswerSerializer
from .models import Commune, BookCategory, Review, User, Direction, Book, ReviewLike, Forum, ForumUser, ForumCategory, Follow, Followed, Discussion, Question, Comments, Answer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.signing import Signer
from django.shortcuts import redirect
import base64

@api_view(['GET']) 
def getCommunes(request):
    comune = Commune.objects.all()
    comunasSerial = CommuneSerializer(comune, many=True)
    return Response(comunasSerial.data)

@api_view(['GET']) 
def getCategories(request):
    category = BookCategory.objects.all()
    categorySerial = BookCategorySerializer(category, many=True)
    return Response(categorySerial.data)

@api_view(['GET']) 
def getReviews(request):
    review = Review.objects.all()
    reviewSerial = ReviewSerializer(review, many=True)
    return Response(reviewSerial.data)

@api_view(['GET'])
@csrf_exempt
def obtainUser(request, token):
    if request.method == 'GET':
        try:
            token1 = Token.objects.get(key = token)
            user = User.objects.get(email = token1.user)
            if user:
                serialUser = userSerializer(user, many=False)
                img_path = 'media/' + str(user.user_photo)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as image_file:
                        image_data = image_file.read()
                        image_base64 = base64.b64encode(image_data)
                        format = get_image_format(img_path)
                else:
                    image_base64 = None   
                    
                user_data = {
                    'id': serialUser.data['id'],
                    'first_name': serialUser.data['first_name'],
                    'last_name': serialUser.data['last_name'],
                    'user_photo': image_base64,
                    'format' : format
                    }
                # Obtén la dirección del usuario y agrégala a los datos de usuario
                user_direction = Direction.objects.get(id=user.id)
                direction_data = {
                    'nombre': user_direction.nombre,
                    'calle': user_direction.calle,
                    'numero': user_direction.numero,
                    'commune': user_direction.commune.id  # Ajusta esto según tus necesidades
                }
                user_data['direction'] = direction_data
                return Response({'msj': 'Autenticación exitosa', 'userData': user_data}, status=status.HTTP_200_OK, content_type=f"image/{format}")
            else:
                return Response({'msj': 'El usuario no existe o la contraseña es incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
        except token1.DoesNotExist:
            return Response({'msj': 'Token Invalido'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def obtainDirection(request, user_id):
    try:
        user = User.objects.get(email=request.user.username)
        direct = Direction.objects.get(user_id = user.id )
        dirSerial = DirectionSerializer(direct, many=False)
        return Response({'userData':dirSerial.data}, status=status.HTTP_200_OK)
    except user.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
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
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reviews(request):
    try:
        # Obtén el usuario autenticado
        user = User.objects.get(email=request.user.username)

        # Obtén todos los libros creados por el usuario
        review = Review.objects.filter(user=user)

        # Serializa los libros para convertirlos en datos JSON
        serializer = ReviewSerializer(review, many=True)

        # Devuelve la lista de libros en la respuesta
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'No se encontraron libros para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reviews_likes(request, id):
    try:
        user = User.objects.get(email = request.user.username)
        review = Review.objects.get(id = id)
        if review:
            like = False
            reviewL = ReviewLike.objects.filter(review = review)
            for review_like in reviewL:
                if review_like.user == user:
                    like = True
                    break
            Likes = reviewL.count()
            return Response({'user_like': like, 'likes': Likes})    
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except review.DoesNotExist:
        return Response({'error': 'No existe la reseña.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_forums(request):
    try:
        forums = Forum.objects.all()
        serialized_forums = ForumSerializer(forums, many=True)    
        return Response({'ForumsData': serialized_forums.data})
    except Exception as e:
        return Response({'error': f'Ha ocurrido un error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_forums(request, user_id):
    try:
        # Obtén el usuario específico por su ID
        user = User.objects.get(id=user_id)

        # Obtén todos los foros a los que se ha unido el usuario y selecciona los campos deseados
        user_forums = ForumUser.objects.filter(user=user).values('forum__id', 'forum__name')

        # Serializa los datos de los foros
        forum_data_list = list(user_forums)

        return Response({'UserForumsData': forum_data_list}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forums_by_category(request, category_id):
    try:
        # Obtén los foros por categoría
        forums = Forum.objects.filter(forum_category=category_id)

        # Serializa los foros para convertirlos en datos JSON
        serializer = ForumSerializer(forums, many=True)

        # Devuelve la lista de foros en la respuesta
        return Response(serializer.data)
    except Forum.DoesNotExist:
        return Response({'error': 'No se encontraron foros para esta categoría.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_forum_categories(request):
    try:
        # Obtén todas las categorías de los foros
        categories = ForumCategory.objects.all()

        # Serializa las categorías para convertirlas en datos JSON
        serializer = ForumCategorySerializer(categories, many=True)

        # Devuelve la lista de categorías en la respuesta
        return Response(serializer.data)
    except ForumCategory.DoesNotExist:
        return Response({'error': 'No se encontraron categorías de foros.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forum_users(request):
    # Obtén todos los usuarios del foro
    forum_users = ForumUser.objects.all()

    # Serializa los usuarios y devuelve una respuesta
    forum_users_serialized = ForumUserSerializer(forum_users, many=True)
    return Response({'ForumUsersData': forum_users_serialized.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_one_forum(request, forum_id):
    try:
        # Obtén el foro específico
        forum = Forum.objects.get(id=forum_id)

        # Obtén todos los usuarios que se han unido a ese foro con el campo 'id'
        forum_users = ForumUser.objects.filter(forum=forum).values('user__id')

        # Serializa los datos de los usuarios utilizando el userSerializer
        user_data_list = sellerSerializer(User.objects.filter(id__in=forum_users), many=True)

        return Response({'ForumUsersData': user_data_list.data}, status=status.HTTP_200_OK)

    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def get_Follows_followers(request):
    if request.method == 'GET':
        try:
            
            user = User.objects.get(email = request.user.username)
        
            followers = Follow.objects.filter(user = user).count()
            follows = Followed.objects.filter(user = user).count()
        
            flsSerial =  FollowedSerializer(follows, many=True)
            flrsSerial = FollowSerializer(followers, many=True)

            return Response({'Follows': flsSerial, 'Followeds': flrsSerial})
        except user.DoesNotExist:
            return Response('El usuario no existe', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forum_discussions(request, forum_id):
    try:
        # Obtén todas las discusiones para el foro dado
        discussions = Discussion.objects.filter(forum_user__forum_id=forum_id)

        if discussions.exists():
            discussions_serialized = DiscussionSerializer(discussions, many=True)
            return Response({'ForumDiscussionsData': discussions_serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontraron discusiones para este foro.'}, status=status.HTTP_404_NOT_FOUND)

    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def confirm_email(request, token):
    signer = Signer()
    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        if not user.is_active:
            user.is_active = True
            user.save()
            return redirect('http://localhost:5173')    
    except User.DoesNotExist:
        return redirect('http://localhost:5173')
 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_forum_discussions(request, forum_id):
    try:
        # Obtén el usuario autenticado
        user = User.objects.get(email=request.user.username)

        # Obtén todas las discusiones del usuario en el foro específico
        discussions = Discussion.objects.filter(forum_user__forum_id=forum_id, forum_user__user=user)

        if discussions.exists():
            discussions_serialized = DiscussionSerializer(discussions, many=True)
            return Response({'UserForumDiscussionsData': discussions_serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontraron discusiones para este usuario en el foro específico.'}, status=status.HTTP_404_NOT_FOUND)

    except Forum.DoesNotExist:
        return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def BookQuestion(request, bookID):
    try:
        book = Book.objects.get(id=bookID)
        ques = Question.objects.filter(book=book)
        answers = Answer.objects.filter(question__in=ques)

        if ques.exists():
            data = ques.values('id', 'user_id', 'user__first_name', 'description', 'answer__description')

            return Response({'Data': data}, status=status.HTTP_200_OK)
        else:
            return Response({'msj': 'No Hay preguntas para este libro'}, status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({'msj': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_discussions(request, user_id):
    try:
        # Obtén las últimas discusiones creadas por el usuario en el foro
        discussions = Discussion.objects.filter(forum_user__user_id=user_id).order_by('-created_at')[:10]
        discussion_serialized = DiscussionSerializer(discussions, many=True)

        if discussions:
            return Response({'LatestDiscussions': discussion_serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'LatestDiscussions': []}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_discussion_by_id(request, discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        discussion_serializer = DiscussionSerializer(discussion, many=False)
        return Response(discussion_serializer.data, status=status.HTTP_200_OK)
    except Discussion.DoesNotExist:
        return Response({'error': 'La discusión no existe.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Comments  # Asegúrate de importar el modelo de tus comentarios

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request, discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        comments = Comments.objects.filter(discussion=discussion)

        if comments:
            comment_serializer = CommentsSerializer(comments, many=True)  # Serializar todos los comentarios en una lista
            return Response({'Comments': comment_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No hay comentarios para esta discusión'}, status=status.HTTP_204_NO_CONTENT)
    except Discussion.DoesNotExist:
        return Response({'error': 'La discusión no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Comments.DoesNotExist:
        return Response({'message': 'No hay comentarios para esta discusión'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def getimage(request, path):
    # Construye la ruta completa al archivo de imagen en el directorio de medios
    image_path = os.path.join(settings.MEDIA_ROOT, path)

    # Verifica si el archivo existe
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            return Response(image_file.read(), content_type='image/jpeg')  # Ajusta el tipo MIME según el tipo de imagen

    return Response(status=404)