from .serializer import  BookSerializer, sellerSerializer, PurchaseDetailSerializer, PurchaseDetailStateSerializer, ChatRoomSerializer
from .models import Commune, BookCategory, Notification, UserRoom, Auction, PurchaseDetail, Review, User, Direction, Book, ReviewLike, Forum, ForumUser, ForumCategory, Follow, Followed, Discussion, Question, Comments, Answer, ChatRoom, Message, Subscription
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




@api_view(['GET'])
def get_all_sales(request):
    try:
        purchase = PurchaseDetail.objects.all()

        UserRoom.objects.filter()
        def buyer(chatroom, user):
            userroom = UserRoom.objects.filter(chat_room=chatroom).first()
            userroom = UserRoom.objects.filter(chat_room=chatroom).last()
            if userroom.user.id != user.id:
                user = User.objects.get(id = userroom.user.id)
                return user
            elif userroom.user.id != user.id:
                user = User.objects.get(id = userroom.user.id)
                return user
            
        # Serializa las revisiones y convierte las imágenes en base64
        purchase_detail_list = list(
            map(lambda purchases: {
                'id' : purchases.id,
                'purchase_date': purchases.purchase_date,
                'amount': purchases.amount,
                'created_at': purchases.created_at,
                'purchase_detail_state': PurchaseDetailStateSerializer(purchases.purchase_detail_state).data,
                'book': BookSerializer(purchases.book).data,
                'buyer': sellerSerializer(buyer(purchases.chat_room, purchases.book.seller)).data
            }, purchase)
        )

        return Response({'purchases': purchase_detail_list}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({'error': 'No se encontraron revisiones para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)