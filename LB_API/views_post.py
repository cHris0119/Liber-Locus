
from .serializer import BookSerializer, ReviewSerializer, ReviewLikeSerializer, ForumSerializer, FollowedSerializer, FollowSerializer, QuestionSerializer, AnswerSerializer, PaymentMethodSerializer, CommentsSerializer, es_fecha_vencimiento_valida, es_cvv_valido, es_rut_valido
from .models import Book, BookCategory, User, Review, ReviewLike, Forum, ForumCategory, ForumUser, Follow, Followed, Discussion, Comments, Question, Answer, PaymentMethod
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response  
from rest_framework import status
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from django.contrib.auth.models import User as AdminUser
from django.utils import timezone
from django.core.mail import EmailMessage
from django_backend.settings import EMAIL_HOST_USER
from django.core.signing import Signer

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
        # Obtiene la marca de tiempo actual en segundos
        
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
                
            book = Book.objects.create(
                id=int_id(),
                name=data['name'],
                price=data['price'],
                description=data['description'],
                author=data['author'],
                book_img=data['book_img'],
                seller=seller,
                book_state_id=book_state_id,  # Establece el valor predeterminado
                book_category=book_category,
                created_at=datetime.now()
                )
            book_serialized = BookSerializer(book, many=False)
            
            return Response({'BookData': book_serialized.data})
        except BookCategory.DoesNotExist:
            return Response({'error': 'La categoría del libro no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])        
@permission_classes([IsAuthenticated])
def review_create(request):
    if request.method == 'POST':
        data = request.data
        try:
            usuario = User.objects.get(email = request.user.username)
            reviewUser = Review.objects.get(title = data['title'], user = usuario)
            if reviewUser:
                return Response({'error': 'Ya existe esa Reseña'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            try:
                review = Review.objects.create(
                id = int_id(),
                title = data['title'],
                created_at = datetime.now(),
                description = data['description'],
                valoration = data['valoration'],
                updated_at = datetime.now(),
                review_img = data['review_img'],
                user = usuario)
            
                reviewSerial = ReviewSerializer(review, many=False)
                return Response({'reviewData': reviewSerial.data})
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

            forum = Forum.objects.create(
                id=int_id(),
                name=data['name'],
                created_at=datetime.now(),
                forum_img=data.get('forum_img', ''),
                forum_category=forum_category,
                user=user  # Asigna al usuario que creó el foro
            )

            # Añade al usuario como miembro del foro que acaba de crear
            ForumUser.objects.create(id=int_id(),forum=forum, user=user)

            forum_serialized = ForumSerializer(forum, many=False)

            return Response({'ForumData': forum_serialized.data})
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
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
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
    
    
@api_view(['POST'])
def send_email(request, email):
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

        question_serialized = QuestionSerializer(question, many=False)
        return Response({'Question': question_serialized.data}, status=status.HTTP_200_OK)

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

    