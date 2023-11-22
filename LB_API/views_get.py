import os
from .functions import get_image_format, base64_image
from django_backend import settings
from .serializer import CommuneSerializer, AuctionStateSerializer, PurchaseDetailSerializer, BookStateSerializer, buyerSerializer, BookCategorySerializer, ReviewSerializer, userSerializer, DirectionSerializer, BookSerializer, ReviewLikeSerializer, ForumSerializer, ForumCategorySerializer, ForumUserSerializer, FollowSerializer, FollowedSerializer, QuestionSerializer, DiscussionSerializer, sellerSerializer, CommentsSerializer, AnswerSerializer
from .models import Commune, BookCategory, UserRoom, Auction, PurchaseDetail, Review, User, Direction, Book, ReviewLike, Forum, ForumUser, ForumCategory, Follow, Followed, Discussion, Question, Comments, Answer, ChatRoom, Message
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
from django.core.serializers import serialize
import json
from django.db.models import Count


@api_view(['GET']) 
def getCommunes(request):
    comune = Commune.objects.all()
    comunasSerial = CommuneSerializer(comune, many=True)
    return Response(comunasSerial.data)

@api_view(['GET']) 
def getCategories(request):
    category = BookCategory.objects.all()
    if category:
        categorySerial = BookCategorySerializer(category, many=True)
        return Response(categorySerial.data)
        

@api_view(['GET']) 
def getReviews(request):
    reviews = Review.objects.all()
    if reviews:
    # Serializa los datos de las revisiones y los modelos relacionados
        review_data_list = list(
            map(lambda review: {
                'id': review.id,
                'title': review.title,
                'created_at': review.created_at,
                'valoration': review.valoration,
                'user': sellerSerializer(review.user).data,
                'description': review.description,
                'review_img': base64_image('media/' + str(review.review_img)),
                'format': get_image_format('media/' + str(review.review_img))
            }, reviews)
        )
        return Response(review_data_list)
    else:
        review_data_list = []
        return Response(review_data_list)        



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
                format = None
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
    if request.method == 'GET':
        try:
            books = Book.objects.all()
            if books:
                book_data_list = list(
                    map(lambda book: {
                        'id': book.id,
                        'name': book.name,
                        'price': str(book.price),
                        'description': book.description,
                        'author': book.author,
                        'created_at': book.created_at,
                        'seller': sellerSerializer(book.seller).data,  # Serializa al vendedor
                        'book_category': BookCategorySerializer(book.book_category).data,  # Serializa la categoría
                        'book_state': BookStateSerializer(book.book_state).data,
                        'book_img': base64_image('media/' + str(book.book_img)),
                        'format': get_image_format('media/' + str(book.book_img))
                    }, books)
                )

                return Response({'books': book_data_list}, status=status.HTTP_200_OK)
            else:
                book_data_list = []
                return Response({'books': book_data_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_books(request):
    try:
        # Obtén el usuario autenticado
        user = User.objects.get(email=request.user.username)

        # Obtén todos los libros creados por el usuario
        books = Book.objects.filter(seller=user)

        # Serializa los libros y convierte las imágenes en base64
        book_data_list = list(
            map(lambda book: {
                'id': book.id,
                'name': book.name,
                'price': str(book.price),
                'description': book.description,
                'author': book.author,
                'created_at': book.created_at,
                'seller': sellerSerializer(book.seller).data,  # Serializa al vendedor
                'book_category': BookCategorySerializer(book.book_category).data,  # Serializa la categoría
                'book_state': BookStateSerializer(book.book_state).data,
                'book_img': base64_image('media/' + str(book.book_img)),
                'format': get_image_format('media/' + str(book.book_img))
            }, books)
        )

        return Response({'books': book_data_list}, status=status.HTTP_200_OK)
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

        # Obtén todas las revisiones creadas por el usuario
        reviews = Review.objects.filter(user=user)

        # Serializa las revisiones y convierte las imágenes en base64
        review_data_list = list(
            map(lambda review: {
                'id': review.id,
                'title': review.title,
                'created_at': review.created_at,
                'valoration': review.valoration,
                'user': sellerSerializer(review.user).data,
                'description': review.description,
                'review_img': base64_image('media/' + str(review.review_img)),
                'format': get_image_format('media/' + str(review.review_img))
            }, reviews)
        )

        return Response({'reviews': review_data_list}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({'error': 'No se encontraron revisiones para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
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
        user = User.objects.get(email = request.user.username)
        forums = Forum.objects.all()

        # Serializa los foros y convierte las imágenes en base64
        forum_data_list = list(
            map(lambda forum: {
                'id': forum.id,
                'name': forum.name,
                'created_at': forum.created_at,
                'forum_category': ForumCategorySerializer(ForumCategory.objects.get(id=forum.forum_category_id)).data['id'],
                'user': sellerSerializer(forum.user).data,
                'forum_img': base64_image('media/' + str(forum.forum_img)),
                'format': get_image_format('media/' + str(forum.forum_img))
                # Agrega otros campos del foro aquí según tu modelo
            }, forums)
        )

        return Response({'ForumsData': forum_data_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Ha ocurrido un error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_forums(request, user_id):
    try:
        # Obtén el usuario específico por su ID
        user = User.objects.get(id=user_id)

        # Obtén todos los foros a los que se ha unido el usuario y selecciona los campos deseados
        user_forums = ForumUser.objects.filter(user=user)
        if user_forums:
        # Serializa los datos de los foros y las categorías, y convierte las imágenes en base64
            forum_data_list = list(
                map(lambda user_forum: {
                    'id': user_forum.forum.id,
                    'name': user_forum.forum.name,
                    'created_at': user_forum.forum.created_at,
                    'forum_category': ForumCategorySerializer(ForumCategory.objects.get(id=user_forum.forum.forum_category_id)).data['id'],
                    'user': sellerSerializer(user_forum.forum.user).data,
                    'forum_img': base64_image('media/' + str(user_forum.forum.forum_img)),
                    'format': get_image_format('media/' + str(user_forum.forum.forum_img))
                }, user_forums)
            )

            return Response({'UserForumsData': forum_data_list}, status=status.HTTP_200_OK)
        else:
            forum_data_list = []
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

        # Serializa los foros y convierte las imágenes en base64
        forum_data_list = list(
            map(lambda forum: {
                'forum_id': forum.id,
                'name': forum.name,
                'created_at': forum.created_at,
                'forum_category': ForumCategorySerializer(ForumCategory.objects.get(id=forum.forum_category_id)).data['id'],
                'forum_img': base64_image('media/' + str(forum.forum_img)),
                'format': get_image_format('media/' + str(forum.forum_img))
                # Agrega otros campos del foro aquí según tu modelo
            }, forums)
        )

        return Response({'ForumsData': forum_data_list}, status=status.HTTP_200_OK)
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
            return Response({'Data': []}, status=status.HTTP_200_OK)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_purchases(request):
    try:
        # Obtén el usuario utilizando el ID de la sesión en la respuesta
        user = User.objects.get(email=request.user.username)

        # Filtra todas las compras donde el usuario es comprador
        user_purchases_as_buyer = PurchaseDetail.objects.filter(
            chat_room__userroom__user=user
        ).exclude(book__seller=user)

        # Verifica si hay compras para el usuario como comprador
        if not user_purchases_as_buyer.exists():
            return Response({'message': 'No hay compras para este usuario como comprador.'}, status=status.HTTP_404_NOT_FOUND)

        # Serializa el queryset con la información del vendedor y comprador
        serialized_purchases = []
        for purchase in user_purchases_as_buyer:
            seller_info = purchase.book.seller

            serialized_purchase = {
                'id': purchase.id,
                'seller': {
                    'id': seller_info.id,
                    'first_name': seller_info.first_name,
                    'last_name': seller_info.last_name,
                },
                'buyer': {
                    'id': user.id,  # Utiliza el ID del usuario autenticado
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'purchase_date': purchase.purchase_date,
                'amount': purchase.amount,
                'created_at': purchase.created_at,
                'chat_room': purchase.chat_room.id,
                'auction': None,  # Asegúrate de manejar correctamente la propiedad 'auction'
                'book': {
                    'id': purchase.book.id,
                    'name': purchase.book.name,
                    'price': purchase.book.price,
                    'state': purchase.purchase_detail_state.state,
                    'format': get_image_format('media/' + str(purchase.book.book_img)),
                    'book_img': base64_image('media/' + str(purchase.book.book_img))
                },
            }
            serialized_purchases.append(serialized_purchase)

        # Devuelve la información de compras en el formato deseado
        return Response({'compras': serialized_purchases}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'message': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error al obtener las compras: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_sales(request):
    try:
        # Obtén el usuario utilizando el ID de la sesión en la respuesta
        user = User.objects.get(email=request.user.username)

        # Filtra todas las ventas donde el usuario es vendedor
        user_sales_as_seller = PurchaseDetail.objects.filter(
            chat_room__userroom__user=user,
            book__seller=user
        )

        # Verifica si hay ventas para el usuario como vendedor
        if not user_sales_as_seller.exists():
            return Response({'message': 'No hay ventas para este usuario como vendedor.'}, status=status.HTTP_404_NOT_FOUND)

        # Serializa el queryset con la información del comprador y vendedor
        serialized_sales = []
        for sale in user_sales_as_seller:
            buyer_info = sale.chat_room.userroom_set.exclude(user=user).first().user

            serialized_sale = {
                'id': sale.id,
                'seller': {
                    'id': user.id,  # Utiliza el ID del usuario autenticado
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'buyer': {
                    'id': buyer_info.id,
                    'first_name': buyer_info.first_name,
                    'last_name': buyer_info.last_name,
                },
                'purchase_date': sale.purchase_date,
                'amount': sale.amount,
                'created_at': sale.created_at,
                'chat_room': sale.chat_room.id,
                'auction': None,  # Asegúrate de manejar correctamente la propiedad 'auction'
                'book': {
                    'id': sale.book.id,
                    'name': sale.book.name,
                    'price': sale.book.price,
                    'state': sale.purchase_detail_state.state,
                    'format': get_image_format('media/' + str(sale.book.book_img)),
                    'book_img': base64_image('media/' + str(sale.book.book_img))
                },
            }
            serialized_sales.append(serialized_sale)

        # Devuelve la información de ventas en el formato deseado
        return Response({'ventas': serialized_sales}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'message': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error al obtener las ventas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages_chatroom(request, chat_id):
    try:
        chat = ChatRoom.objects.get(id = chat_id)
        message = Message.objects.filter(chat_room=chat)
        message_data_list = list(
            map(lambda message: {
                'id': message.id,
                'message': message.content,
                'created_at': message.created_at,
                'user_id': message.user.id,
                'username': message.user.email,
            }, message)
        )
        return Response({'message':message_data_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_auctions(request):
    if request.method == 'GET':
        try:
            auctions = Auction.objects.all()
            if auctions:
                auction_data_list = list(
                    map(lambda auction: {
                        'id': auction.id,
                        'initial_price': str(auction.initial_price),
                        'created_at': auction.created_at,
                        'duration_days': auction.duration_days,
                        'final_price': str(auction.final_price) if auction.final_price else None,
                        'auction_state': AuctionStateSerializer(auction.auction_state).data,
                        'book': BookSerializer(auction.book).data,  # Serializa el libro asociada
                        'format': get_image_format('media/' + str(auction.book.book_img)),
                        'book_img': base64_image('media/' + str(auction.book.book_img))
                        
                    }, auctions)
                )

                return Response({'auctions': auction_data_list}, status=status.HTTP_200_OK)
            else:
                auction_data_list = []
                return Response({'auctions': auction_data_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_popular_forums(request):
    try:
        user = User.objects.get(email = request.user.username)
        # Ordena los foros por la cantidad de usuarios en orden descendente
        forums = Forum.objects.annotate(user_count=Count('user')).order_by('-user_count')

        # Serializa los foros y convierte las imágenes en base64
        forum_data_list = list(
            map(lambda forum: {
                'id': forum.id,
                'name': forum.name,
                'created_at': forum.created_at,
                'forum_category': ForumCategorySerializer(ForumCategory.objects.get(id=forum.forum_category_id)).data['id'],
                'user_count': forum.user_count,  # Agrega la cantidad de usuarios
                'user': sellerSerializer(forum.user).data,
                'forum_img': base64_image('media/' + str(forum.forum_img)),
                'format': get_image_format('media/' + str(forum.forum_img))
            }, forums)
        )

        return Response({'ForumsData': forum_data_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Ha ocurrido un error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)