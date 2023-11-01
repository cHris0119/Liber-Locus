
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review, User, Auction, AuctionOffer
import time
def int_id():
    # Obtener el tiempo actual en segundos desde la época (timestamp)
    timestamp = int(time.time())
    # Formatear el timestamp como DDMMSS
    formatted_time = time.strftime("%d%H%m%S", time.localtime(timestamp))
    # Convertir la cadena formateada a un número entero
    return int(formatted_time)

class LikesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        self.close()
    
    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        
        if action == 'like':
            user_id = data.get('id')
            review_id = data.get('review_id')
            try:
                user = User.objects.get(id=user_id)
                review = Review.objects.get(id=review_id)
                like = ReviewLike.objects.filter(user=user, review=review).exists()
                likes = ReviewLike.objects.filter(review=review).count()
                if likes == 0:
                    ReviewLike.objects.create(
                        id = int_id(),
                        user = user,
                        review = review
                        )
                    like = ReviewLike.objects.filter(user=user, review=review).exists()
                    likes = ReviewLike.objects.filter(review=review).count()
                    self.send(text_data=json.dumps({
                        'user_like': like,
                        'likes': likes}))
                else:
                    if like:
                        likeus = ReviewLike.objects.get(user=user, review=review)
                        likeus.delete()
                        like = ReviewLike.objects.filter(user=user, review=review).exists()
                        likes = ReviewLike.objects.filter(review=review).count()
                        self.send(text_data=json.dumps({
                        'user_like': like, 
                        'likes': likes}))
                    else:
                        ReviewLike.objects.create(
                        id = int_id(),
                        user = user,
                        review = review
                        )
                        like = ReviewLike.objects.filter(user=user, review=review).exists()
                        likes = ReviewLike.objects.filter(review=review).count()
                        self.send(text_data=json.dumps({
                        'user_like': like, 
                        'likes': likes}))

            except User.DoesNotExist:
        # Handle user not found error
                pass

            except Review.DoesNotExist:
        # Handle review not found error
                pass

class SubastaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['subasta_id']
        self.room_group_name = f"subasta_{self.room_name}"

        try:
            self.subasta = Auction.objects.get(id=self.room_name)
        except Auction.DoesNotExist:
            await self.close()

        if not self.scope['user'].is_authenticated:
            await self.close()

        if self.subasta.book.seller != self.scope['user']:
            await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje_tipo = data['tipo']

        if mensaje_tipo == 'puja':
            puja_monto = data['monto']

            try:
                nueva_puja = AuctionOffer(auction=self.subasta, amount=puja_monto, user=self.scope['user'])
                nueva_puja.save()
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'tipo': 'error',
                    'mensaje': 'Error al procesar la puja.',
                }))
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'enviar_puja',
                    'puja_id': nueva_puja.id,
                    'monto': nueva_puja.amount,
                    'usuario': self.scope['user'].username,
                }
            )

    async def enviar_puja(self, event):
        puja_id = event['puja_id']
        monto = event['monto']
        usuario = event['usuario']

        await self.send(text_data=json.dumps({
            'tipo': 'nueva_puja',
            'puja_id': puja_id,
            'monto': monto,
            'usuario': usuario,
        }))