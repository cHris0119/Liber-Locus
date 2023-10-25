from .serializer import CommuneSerializer, BookCategorySerializer, ReviewSerializer, userSerializer, DirectionSerializer, BookSerializer, ReviewLikeSerializer, ForumSerializer, ForumCategorySerializer, ForumUserSerializer, FollowSerializer, FollowedSerializer, QuestionSerializer, DiscussionSerializer, sellerSerializer
from .models import Commune, BookCategory, Review, User, Direction, Book, ReviewLike, Forum, ForumUser, ForumCategory, Follow, Followed, Discussion, Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.signing import Signer
from django.shortcuts import redirect

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
                user_data = {
                    'id': serialUser.data['id'],
                    'first_name': serialUser.data['first_name'],
                    'last_name': serialUser.data['last_name'],
                    'user_photo': serialUser.data['user_photo']
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
                return Response({'msj': 'Autenticación exitosa', 'userData': user_data}, status=status.HTTP_200_OK)
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

            return Response({'Follows': followers, 'Followeds': follows})
        except user.DoesNotExist:
            return Response('El usuario no existe', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def get_Follows_followers_users(request, user_id):
    if request.method == 'GET':
        try:
            
            user = User.objects.get(id = user_id)
        
            followers = Follow.objects.filter(user = user).count()
            follows = Followed.objects.filter(user = user).count()

            return Response({'Follows': followers, 'Followeds': follows})
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
        book = Book.objects.get(id = bookID)
        try:
            ques = Question.objects.filter(book = book)
            cantidad = ques.count()
            if ques:
                if cantidad > 1:
                    quesSerial =  QuestionSerializer(ques, many=True)
                    return Response({'Questions':quesSerial.data}, status=status.HTTP_200_OK)
                if cantidad == 1:
                    onlyQuest = Question.objects.get(book = book)
                    quesSerial =  QuestionSerializer(onlyQuest, many=False)
                    return Response({'Questions':quesSerial.data}, status=status.HTTP_200_OK)
            else:
                return Response({'msj':'No Hay preguntas para este libro'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_discussions(request, user_id):
    try:
        # Obtén las últimas discusiones creadas por el usuario en el foro
        discussions = Discussion.objects.filter(forum_user__user_id=user_id).order_by('-created_at')[:10]

        if discussions:
            discussion_serialized = DiscussionSerializer(discussions, many=True)
            return Response({'LatestDiscussions': discussion_serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No se encontraron discusiones.'}, status=status.HTTP_204_NO_CONTENT)
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