
from .serializer import BookSerializer, AuctionStateSerializer, ReviewSerializer, ReviewLikeSerializer, ForumSerializer, AuctionOfferSerializer, FollowedSerializer, FollowSerializer, QuestionSerializer, AnswerSerializer, PaymentMethodSerializer, CommentsSerializer, es_fecha_vencimiento_valida, es_cvv_valido, es_rut_valido
from .models import Book, BookCategory, User, BookState, Review, ReviewLike, Forum, ForumCategory, ForumUser,Auction, Follow, Followed, Discussion, Comments, Question, Answer, PaymentMethod, AuctionOffer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime, timedelta
from django.contrib.auth.models import User as AdminUser
from django.utils import timezone
from django.core.mail import EmailMessage
from django_backend.settings import EMAIL_HOST_USER
from django.core.signing import Signer
from PIL import Image
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from .functions import *
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def int_id():
    # Obtener el tiempo actual en segundos desde la época (timestamp)
    timestamp = int(time.time())
    # Formatear el timestamp como DDMMSS
    formatted_time = time.strftime("%d%H%m%S", time.localtime(timestamp))
    # Convertir la cadena formateada a un número entero
    return int(formatted_time)

# Creacion de libros

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    if request.method == 'POST':
        data = request.data
        try:
            # Obtén el vendedor a partir del correo electrónico del usuario autenticado
            user_email = request.user.username
            seller = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'El vendedor no existe'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Configura el valor predeterminado para BOOK_STATE_id
            book_state_id = 2  # Valor predeterminado deseado
            book_category = BookCategory.objects.get(id=data['book_category'])


            # Verifica si se proporciona una imagen en formato base64
            image_data = data.get('book_img', '')
            if image_data.startswith("data:image"):
                try:
                    # Extrae la parte base64 de la cadena de datos de la imagen
                    image_parts = image_data.split(";base64,")
                    image_format = image_parts[0].split("/")[1]
                    image_data = image_parts[1]

                    # Decodifica la imagen y la guarda en el modelo Book
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))

                    book = Book.objects.create(
                        id=int_id(),
                        name=data['name'],
                        price=data['price'],
                        description=data['description'],
                        author=data['author'],
                        seller=seller,
                        book_state_id=book_state_id,  # Establece el valor predeterminado
                        book_category=book_category,
                        created_at=datetime.now()
                    )

                    image_filename = f"{book.id}.{image_format}"
                    book.book_img.save(image_filename, ContentFile(image_bytes), save=True)

                    imgb64 = base64.b64encode(image_bytes).decode('utf-8')
                    book_serialized = BookSerializer(book, many=False)

                    return Response({'BookData': book_serialized.data, 'img': imgb64, 'format': image_format})
                except Exception as e:
                    return Response({'error': f'Error al decodificar y guardar la imagen: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Los datos de la imagen del libro no están en el formato correcto'}, status=status.HTTP_400_BAD_REQUEST)

        except BookCategory.DoesNotExist:
            return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al crear el libro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create(request):
    if request.method == 'POST':
        data = request.data
        try:
            usuario = User.objects.get(email=request.user.username)

            # Verifica si se proporciona una imagen en formato base64
            image_data = data['review_img']
            if image_data.startswith("data:image"):
                try:
                    # Extrae la parte base64 de la cadena de datos de la imagen
                    image_parts = image_data.split(";base64,")
                    image_format = image_parts[0].split("/")[1]
                    image_data = image_parts[1]

                    # Decodifica la imagen y la guarda en el modelo Review
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))

                    review = Review.objects.create(
                        id=int_id(),
                        title=data['title'],
                        created_at=datetime.now(),
                        description=data['description'],
                        valoration=data['valoration'],
                        updated_at=datetime.now(),
                        user=usuario
                    )

                    # Asegúrate de utilizar la extensión correcta para el archivo de imagen
                    review_img_filename = f"{review.id}.{image_format}"
                    review.review_img.save(review_img_filename, ContentFile(image_bytes), save=True)
                    review.save()

                    reviewSerial = ReviewSerializer(review, many=False)
                    imgb64 = base64.b64encode(image_bytes)             
                    return Response({'reviewData': reviewSerial.data, 'img':imgb64, 'format':image_format})
                except Exception as e:
                    return Response({'error': 'Error al decodificar y guardar la imagen'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Los datos de la imagen de la reseña no están en el formato correcto'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])        
@permission_classes([IsAuthenticated])        
def like_a_post(request, id):
    if request.method == 'POST':
        user = User.objects.get(email = request.user.username)
        review = Review.objects.get(id = id)
        if user:
            try:
                reviewLike = ReviewLike.objects.create(
                    id = int_id(),
                    user = user,
                    review = review   
                )
                RSerial = ReviewLikeSerializer(reviewLike, many=False)
                return Response(RSerial.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_forum(request):
    if request.method == 'POST':
        data = request.data

        try:
            # Obtén el usuario autenticado
            user = User.objects.get(email=request.user.username)

        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Configura el valor predeterminado para FORUM_CATEGORY_id
            forum_category = ForumCategory.objects.get(id=data['forum_category'])

            # Verifica si se proporciona una imagen en formato base64
            image_data = data['forum_img']
            if image_data.startswith("data:image"):
                try:
                    # Extrae la parte base64 de la cadena de datos de la imagen
                    image_parts = image_data.split(";base64,")
                    image_format = image_parts[0].split("/")[1]
                    image_data = image_parts[1]

                    # Decodifica la imagen y la guarda en el modelo Forum
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))

                    forum = Forum.objects.create(
                        id=int_id(),
                        name=data['name'],
                        created_at=datetime.now(),
                        forum_category=forum_category,
                        user=user  # Asigna al usuario que creó el foro
                    )

                    # Asegúrate de utilizar la extensión correcta para el archivo de imagen
                    forum_img_filename = f"{forum.id}.{image_format}"
                    forum.forum_img.save(forum_img_filename, ContentFile(image_bytes), save=True)
                    forum.save()

                    # Añade al usuario como miembro del foro que acaba de crear
                    ForumUser.objects.create(id=int_id(), forum=forum, user=user)
                    
                    forum_serialized = ForumSerializer(forum, many=False)
                    imgb64 = base64.b64encode(image_bytes)          
                    return Response({'ForumData': forum_serialized.data, 'img': imgb64, 'format':image_format})
                except Exception as e:
                    print(str(e))
                    return Response({'error': 'Error al decodificar y guardar la imagen'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Los datos de la imagen del foro no están en el formato correcto'}, status=status.HTTP_400_BAD_REQUEST)

        except ForumCategory.DoesNotExist:
            return Response({'error': 'La categoría del foro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_forum(request, id):
    if request.method == 'POST':
        user = User.objects.get(email=request.user.username)
        forum = Forum.objects.get(id=id)
        if user:
            # Verifica si el usuario ya es miembro del foro
            if ForumUser.objects.filter(user=user, forum=forum).exists():
                return Response({'message': 'Ya eres miembro de este foro.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                forum_user = ForumUser.objects.create(
                    id=int_id(),
                    user=user,
                    forum=forum
                )
                return Response({'message': 'Te has unido al foro exitosamente.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Hubo un error al unirse al foro'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
@permission_classes({IsAuthenticated})
def followUser(request, idUser):
    try:
        
        follow = User.objects.get(email = request.user.username)
        followed = User.objects.get(id = idUser)
        
        followeds = Followed.objects.create(
            id = int_id(),
            user = followed
        )
        followModel = Follow.objects.create(
            id = int_id(),
            user = follow,
            followed = followeds
        )
        return Response(f'Le has dado like a {followed.email}', status=status.HTTP_200_OK)        
    except follow.DoesNotExist:
        return Response('Hubo un error al seguir a la persona', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
def send_email(email):
    try:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("No se encontró un usuario con esa dirección de correo electrónico.", status=status.HTTP_400_BAD_REQUEST)
        signer = Signer()
        token = signer.sign(user.email)
        user.confirm_key = token
        user.save()
        mail = user.email
        url = f'http://127.0.0.1:8000/LB_API/api/users/confirm_email/{token}/'
        email = EmailMessage(
        f'Bienvenido a LiberLocus {mail}',
        f'Para continuar con el inicio de sesión debemos verificar su correo\n\n {url} \n\n',
        f"<{EMAIL_HOST_USER}>",
        [mail]
        )
        try:
            email.send(fail_silently=True)
            print(email)
            return Response('Correo de confirmación enviado con éxito', status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
    
       

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_discussion(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.user.username)

            # Asegúrate de que el usuario existe
            if not user:
                return Response({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)

            forum_id = request.data.get('forum_id')

            # Asegúrate de que el foro exista
            forum = Forum.objects.get(id=forum_id)

            if not forum:
                return Response({'error': 'El foro no existe.'}, status=status.HTTP_404_NOT_FOUND)

            # Asegúrate de que el usuario sea miembro del foro
            if not ForumUser.objects.filter(user=user, forum=forum).exists():
                return Response({'error': 'El usuario no es miembro de este foro.'}, status=status.HTTP_403_FORBIDDEN)

            title = request.data.get('title')
            description = request.data.get('description')

            # Crea la discusión y asigna al usuario actual como el creador
            discussion = Discussion.objects.create(
                id=int_id(),
                title=title,
                description=description,
                created_by=user,  # Asigna al usuario actual como el creador
                created_at=datetime.now(),
                forum_user=ForumUser.objects.get(user=user, forum=forum)
            )

            return Response({'message': 'Discusión creada exitosamente.', 'discussion_id': discussion.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request, discussion_id):
    # Obtén la discusión específica
    discussion = Discussion.objects.get(id=discussion_id)
    
    user = User.objects.get(email=request.user.username)  # Obtén al usuario autenticado
    
    if request.method == 'POST':
        content = request.data.get('content')
        
        # Crea el comentario
        comment = Comments.objects.create(
            id=int_id(),
            content=content,
            created_at=datetime.now(),
            discussion=discussion,
            user=user
        )

        # Serializa el comentario para incluirlo en la respuesta
        comment_serializer = CommentsSerializer(comment)
        
        return Response({'message': 'Comentario agregado exitosamente', 'comment': comment_serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def askQuestion(request, bookID):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        book = Book.objects.get(id=bookID)

        if user == book.seller:
            return Response({'error': 'Eres el vendedor del libro. No puedes hacer preguntas.'}, status=status.HTTP_400_BAD_REQUEST)

        question = Question.objects.create(
            id=int_id(),
            description=data['description'],
            book=book,
            user=user
        )

        # Obtén el nombre del usuario que creó la pregunta
        id_author = user.id
        author_name = user.first_name

        question_serialized = QuestionSerializer(question, many=False)
        response_data = {
            'Question': question_serialized.data,
            'id': id_author,
            'Author': author_name  # Agregar el nombre del autor
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createAnswer(request, Q_id):
    try:
        data = request.data
        user = User.objects.get(email=request.user.username)
        question = Question.objects.get(id=Q_id)
        book = Book.objects.get(id=question.book.id)

        if user == book.seller:
            try:
                answer = Answer.objects.create(
                    id=int_id(),
                    description=data['description'],
                    question=question,
                    user=user
                )

                answer_serialized = AnswerSerializer(answer, many=False)
                return Response({'Answer': answer_serialized.data}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No estás autorizado para responder a la pregunta'}, status=status.HTTP_401_UNAUTHORIZED)

    except Question.DoesNotExist:
        return Response({'error': 'La pregunta no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Book.DoesNotExist:
        return Response({'error': 'El libro no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_method(request):
    serializer = PaymentMethodSerializer(data=request.data)

    if serializer.is_valid():
        # Verificar si el método de pago ya existe para el usuario actual
        existing_payment_method = PaymentMethod.objects.filter(user=request.user, card_number=serializer.validated_data['card_number']).first()
        if existing_payment_method:
            return Response({"error": "Ya existe un método de pago con este número de tarjeta para este usuario."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar la fecha de vencimiento y el CVV
        expiration_month = serializer.validated_data['expiration_month']
        expiration_year = serializer.validated_data['expiration_year']
        cvv = serializer.validated_data['cvv']

        if not es_fecha_vencimiento_valida(expiration_month, expiration_year):
            return Response({"error": "La fecha de vencimiento no es válida."}, status=status.HTTP_400_BAD_REQUEST)

        if not es_cvv_valido(cvv, serializer.validated_data['method_name']):
            return Response({"error": "El código CVV no es válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar el RUT
        if not es_rut_valido(serializer.validated_data['rut']):
            return Response({"error": "El RUT no es válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Limitar la cantidad de métodos de pago por usuario
        existing_payment_methods_count = PaymentMethod.objects.filter(user=request.user).count()
        if existing_payment_methods_count >= 4:
            return Response({"error": "Se ha alcanzado el límite de métodos de pago permitidos por usuario."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el método de pago
        serializer.save(user=request.user)
        return Response({"message": "Método de pago creado con éxito."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subasta(request, book_id):
    if request.method == 'POST':
        data = request.data

        try:
            # Asegúrate de obtener al usuario autenticado (el vendedor de la subasta)
            seller = User.objects.get(email=request.user.username)

            # Verifica si el usuario tiene un libro específico con el ID proporcionado
            try:
                book = Book.objects.get(id=book_id, seller=seller)
            except Book.DoesNotExist:
                return Response({'error': 'No tienes un libro con el ID especificado en el marketplace.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica si el libro ya está en una subasta
            if book.book_state_id == 3:  # Estado "IN AUCTION"
                return Response({'error': 'El libro ya está en una subasta.'}, status=status.HTTP_400_BAD_REQUEST)

            # Calcular la fecha y hora de finalización de la subasta
            duration_days = data['duration_days']
            end_datetime = datetime.now() + timedelta(days=duration_days)

            # Crea una nueva subasta relacionada con el libro específico
            subasta = Auction.objects.create(
                id=int_id(),
                initial_price=data['initial_price'],
                created_at=datetime.now(),
                duration_days=duration_days,
                final_price=data.get('final_price', None),  # Puedes ajustar esto según tus necesidades
                auction_state_id=2,  # Establece el estado de la subasta a "AVAILABLE" (estado 2)
                book=book
            )

            # Crea un canal único para la subasta
            channel_layer = get_channel_layer()
            group_name = f"auction_{subasta.id}"
            subasta.channel_name = group_name
            subasta.save()

            # Actualiza el estado del libro a "IN AUCTION" (estado 3)
            book.book_state_id = 3
            book.save()

            # Obtén la imagen del libro y su formato en formato base64
            book_image_path = 'media/' + str(subasta.book.book_img)
            book_image = base64_image(book_image_path)
            book_image_format = get_image_format(book_image_path)

            # Serializa el libro actualizado
            book_serialized = BookSerializer(book, many=False)

            #Serializa el estado de la subasta
            # Obtén los datos del estado de la subasta y del libro
            auction_state_serialized = AuctionStateSerializer(subasta.auction_state, many=False)

            response_data = {
                'message': 'Subasta creada exitosamente.',
                'id': subasta.id,
                'initial_price': subasta.initial_price,
                'final_price': subasta.final_price,
                'end_datetime': end_datetime,
                'book': book_serialized.data,
                'auction_state': auction_state_serialized.data,
                'img': book_image,
                'format': book_image_format,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
            

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def realizar_puja(request, subasta_id):
    if request.method == 'POST':
        user = request.user
        subasta = Auction.objects.get(id=subasta_id)
        amount = request.data.get('amount')

        try:
            if subasta.auction_state_id != 2:
                return Response({'error': 'La subasta no está disponible para pujar.'}, status=400)

            ultima_puja = AuctionOffer.objects.filter(auction=subasta).latest('created_at')
            precio_minimo = ultima_puja.amount if ultima_puja else subasta.initial_price

            if amount < precio_minimo:
                return Response({'error': 'El monto de la puja debe ser mayor o igual al precio mínimo.'}, status=400)

            subasta.final_price = amount
            subasta.save()

            auction_offer = AuctionOffer.objects.create(
                id=int_id(),
                auction=subasta,
                user=user,
                amount=amount,
                created_at=timezone.now()
            )

            serializer = AuctionOfferSerializer(auction_offer)
            return Response(serializer.data)

        except Auction.DoesNotExist:
            return Response({'error': 'La subasta especificada no existe.'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finalizar_subasta(request, subasta_id):
    try:
        subasta = Auction.objects.get(id=subasta_id)
        user = User.objects.get(email=request.user.username)

        # Verifica si el usuario autenticado es el vendedor del libro relacionado con la subasta
        es_vendedor = subasta.book.seller == user

        if es_vendedor:
            # Encuentra y elimina todas las ofertas relacionadas con la subasta
            ofertas_subasta = AuctionOffer.objects.filter(auction=subasta)
            ofertas_subasta.delete()

            # Cambia el estado de la subasta a "Finalizada" 
            subasta.auction_state_id = 1  # Asigna el ID correcto del estado "Finalizada"
            subasta.save()

            # Actualiza el estado del libro a "Vendido" 
            subasta.book.book_state_id = 1  # Asigna el ID correcto del estado "Vendido"
            subasta.book.save()

            return Response({'message': 'Subasta finalizada con éxito'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tienes permiso para finalizar esta subasta.'}, status=status.HTTP_403_FORBIDDEN)

    except Auction.DoesNotExist:
        return Response({'error': 'La subasta no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)