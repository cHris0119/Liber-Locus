
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review, User, Auction, AuctionOffer
import time
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync


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

# consumer.py
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Auction, AuctionOffer
from django.utils import timezone

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            subasta_id = data.get('subasta_id')
            subasta = await self.get_subasta(subasta_id)

            if not subasta:
                await self.send(text_data=json.dumps({'error': 'La subasta no existe.'}))
                return

            if subasta.auction_state_id != 2:
                await self.send(text_data=json.dumps({'error': 'La subasta no está disponible para pujar.'}))
                return

            amount = data.get('amount', 0)

            if not isinstance(amount, (int, float)) or amount <= 0:
                await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser un número positivo válido.'}))
                return
            
            if subasta.final_price is None:
                if subasta.initial_price is not None and subasta.initial_price >= amount:
                    await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser mayor a la actual.'}))
                    return
            else:
                if subasta.final_price is not None and subasta.final_price >= amount:
                    await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser mayor a la actual.'}))
                    return
            
            await self.create_puja(subasta, amount)
            
            await self.alter_subasta(amount, subasta_id)

            await self.send(text_data=json.dumps({'message': int(subasta.final_price)}))

        except Auction.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'La subasta especificada no existe.'}))
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    @database_sync_to_async
    def get_subasta(self, subasta_id):
        try:
            return Auction.objects.get(id=subasta_id)
        except Auction.DoesNotExist:
            return None
    @database_sync_to_async
    def alter_subasta(self, amount, subasta_id):
        try:
            auc = Auction.objects.get(id=subasta_id)
            auc.final_price = amount
            auc.save()
        except Auction.DoesNotExist:
            return None

    @database_sync_to_async
    def get_ultima_puja(self, subasta):
        return AuctionOffer.objects.filter(auction=subasta).latest('created_at')

    @database_sync_to_async
    def create_puja(self, subasta, amount):
        us = User.objects.get(id =7191112)
        
        AuctionOffer.objects.create(
                    id=int_id(),
                    auction=subasta,
                    user=us,
                    amount=amount,
                    created_at=timezone.now()
                )
        