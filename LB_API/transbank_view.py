from transbank import webpay
from django_backend.settings import TRANSBANK_COMMERCE_CODE
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_pago(request):
    # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
    monto = float(request.data.get('monto'))
    orden_compra = request.data.get('orden_compra')

    # Configura el SDK de Transbank
    webpay.configuration.configure_for_testing()  # Cambia a producción en entorno de producción

    # Crea una instancia de Webpay Plus Normal
    transaction = webpay.WebpayPlusNormal(TRANSBANK_COMMERCE_CODE, webpay.configuration)
    response = transaction.create(orden_compra, monto, 'http://tu-sitio.com/retorno', 'http://tu-sitio.com/finalizado')

    # Devuelve la URL de redirección para el pago
    return Response({'url': response.url})


def retorno_pago(request):
    # Configura el SDK de Transbank
    webpay.configuration.configure_for_testing()  # Cambia a producción en entorno de producción

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