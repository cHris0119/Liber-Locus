from rest_framework import serializers
from .models import *
import datetime


class userSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = '__all__'
        
class roleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: Role
        fields = '__all__'
        
class userRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: UserRole
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'

class AuctionOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionOffer
        fields = '__all__'

class AuctionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionState
        fields = '__all__'


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


class sellerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name']
class BookSerializer(serializers.ModelSerializer):
    book_category = BookCategorySerializer(many=False, read_only=True,)
    seller = sellerSerializer(many=False, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'description', 'author', 'book_img', 'created_at', 'seller', 'book_category']

class BookStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookState
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = '__all__'

class ForumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumUser
        fields = '__all__'

class DiscussionSerializer(serializers.ModelSerializer):
    forum_user = ForumUserSerializer(many=False, read_only=True)  # Usamos el serializador de ForumUser

    class Meta:
        model = Discussion
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'forum_user']

class FollowedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Followed
        fields = '__all__'
class FollowSerializer(serializers.ModelSerializer):
    followed = FollowedSerializer(many=False)
    class Meta:
        model = Follow
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# COMIENZO DE VALIDACION DEL METODO DE TARJETA 

def es_numero_tarjeta_valido(card_number):
    if not card_number or not card_number.isdigit():
        return False

    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = int(digit) * 2
            total += doubled if doubled < 10 else doubled - 9
        else:
            total += int(digit)

    return total % 10 == 0

def es_fecha_vencimiento_valida(expiration_month, expiration_year):
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month

    return (expiration_year > current_year) or (expiration_year == current_year and expiration_month >= current_month)

def es_cvv_valido(cvv, card_type):
    if not cvv:
        return False

    if not cvv.isdigit():
        return False

    if len(cvv) not in (3, 4):
        return False

    if card_type == 'Visa' and len(cvv) != 3:
        return False
    elif card_type == 'MasterCard' and len(cvv) != 3:
        return False
    # Agrega validaciones para otros tipos de tarjetas

    return True

def es_rut_valido(rut):
    # Eliminar posibles puntos y guiones del RUT y espacios en blanco adicionales.
    rut = rut.replace('.', '').replace('-', '').strip()

    # Verificar que el RUT consta de al menos 8 caracteres (números o "K").
    if not rut.isdigit() or len(rut) < 8:
        return False

    # Separar los números del RUT (sin el dígito verificador) y el dígito verificador.
    rut_numeros = rut[:-1]
    digito_verificador = rut[-1]

    # Calcular el dígito verificador esperado (DV).
    suma = 0
    multiplo = 2
    for d in reversed(rut_numeros):
        valor = int(d) * multiplo
        if valor >= 10:
            valor -= 9
        suma += valor
        multiplo = 2 if multiplo == 1 else 1

    resto = suma % 11
    dv_esperado = 11 - resto if resto != 0 else 0

    # Comparar el dígito verificador calculado con el proporcionado en el RUT.
    if digito_verificador.isdigit():
        return int(digito_verificador) == dv_esperado
    elif digito_verificador.upper() == 'K':
        return dv_esperado == 10

    return False

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

    def validate(self, data):    
        id = data.get('id')
        rut = data.get('rut')
        method_name = data.get('method_name')
        card_number = data.get('card_number')
        expiration_month = data.get('expiration_month')
        expiration_year = data.get('expiration_year')
        cvv = data.get('cvv')
        user = data.get('user')

        # Validación del número de tarjeta
        if not es_numero_tarjeta_valido(card_number):
            raise serializers.ValidationError("El número de tarjeta no es válido.")

        # Validación de la fecha de vencimiento
        if not es_fecha_vencimiento_valida(expiration_month, expiration_year):
            raise serializers.ValidationError("La fecha de vencimiento no es válida.")

        # Validación del CVV
        if not es_cvv_valido(cvv, method_name):
            raise serializers.ValidationError("El código CVV no es válido.")
        
        # Validación del RUT
        if not es_rut_valido(rut):
            raise serializers.ValidationError("El RUT no es válido.")

        return data
    

# TERMINO DE LA VALIDACION DE LA TARJETA

class PostVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVenta
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class PurchaseDetailStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetailState
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'description')

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = sellerSerializer(many=False, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'

class StatePostVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatePostVenta
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthtokenToken
        fields = '__all__'
        
class editUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_photo']
        
class editDirectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Direction
        fields = ['nombre','calle', 'numero', 'commune']

class editBooksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['name', 'price', 'description', 'author', 'book_img', 'book_category']

class editReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'description', 'valoration']