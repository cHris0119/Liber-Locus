from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from .models import PurchaseDetail, PurchaseDetailState, User, ChatRoom, Book, UserRoom, Notification, AuctionOffer, BookState, Auction, Subscription
from .functions import int_id, generar_codigo
from rest_framework import status
from datetime import datetime
from django.shortcuts import redirect
from dotenv import load_dotenv
import os
load_dotenv()
Host = os.environ.get('URL_HOST')

@api_view(['POST'])
def iniciar_pago(request):
    try:
        # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
        amount = request.data.get('monto')
        buy_order = str(request.data.get('orden_compra'))
        return_url = f'http://{Host}:8000/LB_API/api/transbank/retorno/'
        session_id = str(request.data.get('user_id'))
        
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        resp = tx.create(buy_order, session_id,  amount, return_url)
        return Response({'url': resp['url'], 'token':resp['token']})
    except Exception as e:
        return Response({'errorIniciar': str(e)})

@api_view(['GET'])
def retorno_pago(request): 
    pdetail = PurchaseDetailState.objects.get(id = 2)
    token = request.GET['token_ws']
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.commit(token)
    if response.get('status') == 'AUTHORIZED':
        try:
            book = Book.objects.get(id = response.get('buy_order'))
            bookC = BookState.objects.get(id = 1)
            try:
                 chatroom = ChatRoom.objects.get(id =int(response.get('buy_order')))
                 if chatroom:
                     return redirect('http://localhost:5173/detalleEnvio/correct')
            except:
                user = User.objects.get(id = response.get('session_id'))
                chatroom = ChatRoom.objects.create(
                    id = int(response.get('buy_order')),
                    book = book     
                )
                userRoom = UserRoom.objects.create(
                    id = int(response.get('buy_order')),
                    user= user,
                    chat_room=chatroom
                )
                userroom1 = UserRoom.objects.create(
                    id = int_id(),
                    user= book.seller,
                    chat_room=chatroom
                )
                try:
                    auc = Auction.objects.get(id = response.get('buy_order'))
                    if auc:
                        purchase = PurchaseDetail.objects.create(
                            id = response.get('buy_order'),
                            purchase_date=datetime.now(),
                            amount=response.get('amount'),
                            created_at=datetime.now(),
                            chat_room=chatroom,
                            auction=auc,
                            purchase_detail_state=pdetail,
                            book=book,
                            code_verify = generar_codigo()
                        )
                        message = Notification.objects.create(
                            id = response.get('buy_order'),
                            message = f'Su subasta del libro {auc.book.name} ha sido vendida por el precio {auc.final_price}, el dia {datetime.now().strftime("%Y-%m-%d")}',
                            created_at = datetime.now(),
                            is_read = 'no',
                            user = book.seller
                        )
                        book.book_state = bookC
                        book.save()
                        return redirect('http://localhost:5173/detalleEnvio/correct')
                except:
                    purchase = PurchaseDetail.objects.create(
                        id = response.get('buy_order'),
                        purchase_date=datetime.now(),
                        amount=int(response.get('amount')) - 3000,
                        created_at=datetime.now(),
                        chat_room=chatroom,
                        auction=None,
                        purchase_detail_state=pdetail,
                        book=book,
                        code_verify = generar_codigo()
                        
                    )
                    
                    message = Notification.objects.create(
                            id = response.get('buy_order'),
                            message = f'Su libro {book.name} ha sido vendida por el precio {book.price}, el dia {datetime.now().strftime("%Y-%m-%d")}',
                            created_at = datetime.now(),
                            is_read = 'no',
                            user = book.seller
                    )
                    
                    book.book_state = bookC
                    book.save()
                    return redirect('http://localhost:5173/detalleEnvio/correct')
        except Exception as e:
            return redirect('http://localhost:5173/detalleEnvio/incorrect')
        
    else:
        # La transacción fue rechazada
        return redirect('http://localhost:5173/detalleEnvio/incorrect')
    
    
@api_view(['POST'])
def iniciar_pago_suscripcion(request):
    try:
        # Obtén los datos de la solicitud, como el monto a pagar y la orden de compra
        amount = request.data.get('monto')
        buy_order = str(request.data.get('orden_compra'))
        return_url = f'http://{Host}:8000/LB_API/api/transbank/retorno_suscripcion/'  # Asegúrate de cambiar esto a la URL de tu nueva vista de retorno
        session_id = str(request.data.get('user_id'))
        
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
        resp = tx.create(buy_order, session_id,  amount, return_url)
        return Response({'url': resp['url'], 'token':resp['token']})
    except Exception as e:
        return Response({'errorIniciar': str(e)})
    
@api_view(['GET'])
def retorno_pago_suscripcion(request): 
    pdetail = PurchaseDetailState.objects.get(id = 2)
    token = request.GET['token_ws']
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.commit(token)
    if response.get('status') == 'AUTHORIZED':
        try:
            # Obtén la suscripción que el usuario ha comprado
            new_subscription = Subscription.objects.get(id=response.get('buy_order'))

            # Obtén el usuario
            user = User.objects.get(id=response.get('session_id'))

            # Actualiza la suscripción del usuario
            user.subscription = new_subscription
            user.save()

            return redirect('http://localhost:5173/detalleEnvio/correct')
        except Exception as e:
            return Response({'errorRetorno': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # La transacción fue rechazada
        return redirect('http://localhost:5173/detalleEnvio/incorrect')




# views.py

from django.shortcuts import render

def mostrar_formulario(request):
    return render(request, 'mostrar_formulario.html')

def websocket(request):
    return render(request, 'websocket.html')
