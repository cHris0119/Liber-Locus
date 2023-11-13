from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from .models import PurchaseDetail, PurchaseDetailState, User, ChatRoom, Book
from .functions import int_id, intCreation
from rest_framework import status
from rest_framework.parsers import FormParser
from datetime import datetime
from django.shortcuts import redirect


@api_view(['POST'])
def iniciar_pago(request):
    try:
        # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
        amount = request.data.get('monto')
        buy_order = str(request.data.get('orden_compra'))
        return_url = 'http://127.0.0.1:8000/LB_API/api/transbank/retorno/'
        session_id = "sessionid"
        
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        resp = tx.create(buy_order, session_id,  amount, return_url)
        return Response({'url': resp['url'], 'token':resp['token']})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def retorno_pago(request): 
    pdetail = PurchaseDetailState.objects.get(id = 2)
    token = request.GET['token_ws']
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.commit(token)
    if response.get('status') == 'AUTHORIZED':
        
        try:
            # book = Book.objects.get(id = response.get('buy_order'))
            # chatroom = ChatRoom.objects.create(
            #     id = int(response.get('buy_order')),
            #     book = book     
            # )
            # purchase = PurchaseDetail.objects.create(
            #     id = response.get('buy_order'),
            #     purchase_date=datetime.now(),
            #     amount=response.get('amount'),
            #     created_at=datetime.now(),
            #     chat_room=chatroom,
            #     auction=None,
            #     purchase_detail_state=pdetail,
            #     book=book
            # )
            return redirect('http://localhost:5173/detalleEnvio/correct')
        except Exception as e:
            return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # La transacción fue rechazada
        return Response({'message': 'La transacción fue rechazada'})
    
    

# views.py

from django.shortcuts import render

def mostrar_formulario(request):
    return render(request, 'mostrar_formulario.html')

def websocket(request):
    return render(request, 'websocket.html')
