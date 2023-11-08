from transbank import webpay
from django_backend.settings import TRANSBANK_COMMERCE_CODE
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import PurchaseDetail, PurchaseDetailState, User
from .functions import int_id, intCreation
import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_pago(request, book_id):
    # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
    monto = float(request.data.get('monto'))
    orden_compra = request.data.get('orden_compra')

    # Configura el SDK de Transbank
    webpay.configuration.configure_for_testing()  # Cambia a producción en entorno de producción

    # Crea una instancia de Webpay Plus Normal
    transaction = webpay.WebpayPlusNormal(TRANSBANK_COMMERCE_CODE, webpay.configuration)
    response = transaction.create(orden_compra, monto, 'http://127.0.0.1:8000/LB_API/api/retorno_pago/', 'http://tu-sitio.com/finalizado')

    # Devuelve la URL de redirección para el pago
    return Response({'url': response.url})

@api_view(['GET'])
def retorno_pago(request):
    user = User.objects.get(email = request.user.username)
    webpay.configuration.configure_for_testing()  # Cambia a producción en entorno de producción
    resultado_pago = request.GET.get('TBK_RESPUESTA')
    monto_pago = float(request.GET.get('TBK_MONTO'))
    orden_compra = request.GET.get('TBK_ORDEN_COMPRA')
    # Obtén los parámetros de la respuesta de Transbank
    token = request.GET.get('token_ws')

    # Crea una instancia de Webpay Plus Normal
    transaction = webpay.WebpayPlusNormal(TRANSBANK_COMMERCE_CODE, webpay.configuration)
    response = transaction.commit(token)

    if response.get('status') == 'AUTHORIZED':
        # La transacción fue aprobada
        return Response({'message': 'La transacción fue aprobada'})
    else:
        # La transacción fue rechazada
        return Response({'message': 'La transacción fue rechazada'})
    
    
