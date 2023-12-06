from .serializer import  BookSerializer, sellerSerializer, PurchaseDetailSerializer, PurchaseDetailStateSerializer, ChatRoomSerializer, DirectionSerializer
from .models import Commune, BookCategory, Notification, UserRoom, PurchaseDetailState, PurchaseDetail, Review, User, Direction, Book, ReviewLike, Forum, ForumUser, ForumCategory, Follow, Followed, Discussion, Question, Comments, Answer, ChatRoom, Message, Subscription
from rest_framework.decorators import api_view
from rest_framework import status
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from rest_framework.response import Response
from django.shortcuts import redirect
from .functions import get_image_format, base64_image



@api_view(['GET'])
def get_all_sales(request):
    try:
        purchase = PurchaseDetail.objects.all()
        if purchase is None:
            return Response({'purchases': []}, status=status.HTTP_200_OK)

        UserRoom.objects.filter()
        def buyer(chatroom, user):
            userroom = UserRoom.objects.filter(chat_room=chatroom).first()
            userroom1 = UserRoom.objects.filter(chat_room=chatroom).last()
            if userroom.user.id != user.id:
                user = User.objects.get(id = userroom.user.id)
                return user
            elif userroom1.user.id != user.id:
                user = User.objects.get(id = userroom1.user.id)
                return user
        def getDireccion(user):
            try:
                direct = Direction.objects.get(user = user)
                if direct:
                    return direct
            except:
                direct = None
            
            
        # Serializa las revisiones y convierte las imágenes en base64
        purchase_detail_list = list(
            map(lambda purchases: {
                'id' : purchases.id,
                'purchase_date': purchases.purchase_date,
                'amount': purchases.amount,
                'created_at': purchases.created_at,
                'purchase_detail_state': PurchaseDetailStateSerializer(purchases.purchase_detail_state).data,
                'book': BookSerializer(purchases.book).data,
                'buyer': sellerSerializer(buyer(purchases.chat_room, purchases.book.seller)).data,
                'Direction': DirectionSerializer(getDireccion(buyer(purchases.chat_room, purchases.book.seller))).data,
                'format': get_image_format('media/' + str(purchases.book.book_img)),
                'book_img': base64_image('media/' + str(purchases.book.book_img))
            }, purchase)
        )

        return Response({'purchases': purchase_detail_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# Transbank contador
@api_view(['POST'])
def iniciar_pago_contador(request):
    try:
        # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
        amount = request.data.get('monto')
        buy_order = str(request.data.get('orden_compra'))
        return_url = 'http://127.0.0.1:8000/LB_API/api/transbank/retorno_contador/'  # Asegúrate de cambiar esto a la URL de tu nueva vista de retorno
        session_id = str(request.data.get('user_id'))
        
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        resp = tx.create(buy_order, session_id,  amount, return_url)
        return Response({'url': resp['url'], 'token':resp['token']})
    except Exception as e:
        return Response({'errorIniciar': str(e)})
    
@api_view(['GET'])
def retorno_pago_contador(request): 
    token = request.GET['token_ws']
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.commit(token)
    if response.get('status') == 'AUTHORIZED':
        try:
            pdetail = PurchaseDetailState.objects.get(id = 4)
            id = response.get('buy_order')
            monto = response.get('amount')
            user = response.get('session_id')
            p_detail  = PurchaseDetail.objects.get(id = id, amount = monto)
            if p_detail.book.seller.id == user:
                p_detail.purchase_detail_state = pdetail
                p_detail.save()
                return redirect('http://localhost:5173/detalleEnvio/correct')
            else:
                 return Response({'message': 'La transacción fue rechazada, porque no el vendedor no se encuentra'})
        except Exception as e:
            return Response({'errorRetorno': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # La transacción fue rechazada
        return Response({'message': 'La transacción fue rechazada'})


