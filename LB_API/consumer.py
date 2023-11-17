
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review, User, Auction, AuctionOffer, UserRoom, Message, Notification, ChatRoom
from .functions import int_id
from datetime import datetime
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import get_user_model
from django.utils import timezone
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


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = 'auction_%s' % self.auction
        
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        subasta = await self.get_subasta(self.auction)
        await self.channel_layer.group_send(
            self.auction_group_name,
                {
                    'type': 'send_price_update',
                    'message': int(subasta.final_price),
                }
            )
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(            
            self.auction_group_name,
            self.channel_name
        )
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            

            if data['type'] == 'Sell':
                puja = await self.get_ultima_puja(subasta)
                if puja:
                    user_id = data.get('user_id')                     
                    
                
            if data['type'] == 'Pujar':
                subasta_id = data.get('subasta_id')
                user_id = data.get('user_id')
                amount = data.get('amount', 0)
                subasta = await self.get_subasta(subasta_id)
                if not subasta:
                    await self.send(text_data=json.dumps({'error': 'La subasta no existe.'}))
                    return

                if subasta.auction_state_id != 2:
                    await self.send(text_data=json.dumps({'error': 'La subasta no está disponible para pujar.'}))
                    return

                if not isinstance(amount, (int, float)) or amount <= 0:
                    await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser un número positivo válido.'}))
                    return
            
                if subasta.final_price is None:
                    if  subasta.initial_price >= amount:
                        await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser mayor a la actual.'}))
                        return
                else:
                    if subasta.final_price >= amount:
                        await self.send(text_data=json.dumps({'error': 'El monto de la puja debe ser mayor a la actual.'}))
                        return
                    
                await self.alter_subasta(amount, subasta_id)
                subasta1 = await self.get_subasta(subasta_id)

                user = await self.get_user(user_id)
                await self.create_puja(subasta, amount, user)

                await self.channel_layer.group_send(
                    self.auction_group_name,
                    {
                        'type': 'send_price_update',
                        'message': int(subasta1.final_price),
                    }
                )

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
    def get_user(self, user_id):    
        try:
            return User.objects.get(id= user_id)
        except:
            return None
            
    @database_sync_to_async
    def alter_subasta(self, amount, subasta_id):
        try:
            auc = Auction.objects.get(id=subasta_id)
            auc.final_price = amount
            auc.save()
            return auc
        except Auction.DoesNotExist:
            return None

    @database_sync_to_async
    def get_ultima_puja(self, subasta):
        return AuctionOffer.objects.filter(auction=subasta).latest('created_at')

    @database_sync_to_async
    def create_puja(self, subasta, amount, user):
        
        AuctionOffer.objects.create(
                    id=int_id(),
                    auction=subasta,
                    user=user,
                    amount=amount,
                    created_at=timezone.now()
                )
    @database_sync_to_async
    def create_notification(self, user, message):
        Notification.objects.create(
            id=int_id(),
            message=message,
            created_at=timezone.now(),
            is_read='no',
            user=user
        )
    async def send_price_update(self, event):
            await self.send(text_data=json.dumps({'message': event['message']}))
            
            
            
class Chat_Room(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat = self.scope['url_route']['kwargs']['chatroom_id']
        self.chat_group_name = 'chatroom_%s' % self.chat
        user_email = self.scope.get('user').username
        
        
        # if await self.user_chatroom(user, self.chat) == False:
        #     await self.close()
            
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        
        await self.accept()    
        
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(            
            self.chat_group_name,
            self.channel_name
        )
        
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        
        content = data['message']
        user_id = data['username']
        user = await self.get_user(user_id)
        chat = await self.get_chatroom(self.chat)
        
        if user is None:
            await self.send(text_data=json.dumps({'error': 'No se pudo obtener al usuario actual.'}))
            return
        
        if chat is None:
            await self.send(text_data=json.dumps({'error': 'No se pudo obtener el chat.'}))
            return
        # Agrega el mensaje a la base de datos
        content1 = await self.add_message(chat, user, content)
        
        if content1 is None:
            await self.send(text_data=json.dumps({'error': 'No se pudo mandar el mensaje.'}))
            return 
        
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'id': content1.id,
                'message': content1.content,
                'user_id': user.id,
                'username': user.email,
                'timestamp': datetime.now().isoformat(),
            }
        )
        
        
    async def chat_message(self, event):
        # Envía el mensaje al WebSocket del usuario
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'id': event['id'],
            'message': event['message'],
            'user_id':event['user_id'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))
            
        
    @database_sync_to_async
    def user_chatroom(self, user, chatroom_id):
        try:
            chat = ChatRoom.objects.get(id = chatroom_id)
            userroom = UserRoom.objects.filter(user=user, chat_room=chat).exists()
            if userroom:
                return True
            else: 
                return False            
        except:
            return None
        
    @database_sync_to_async  
    def get_chatroom(self, chatroom_id):
        try:
            chat = ChatRoom.objects.get(id = chatroom_id)
            return chat
        except Exception as e:
            return None
        
    @database_sync_to_async   
    def get_user_chat(self, user, chatroom):
        try:
            useroom = UserRoom.objects.get(user = user)
            chat = UserRoom.objects.get(chat_room=chatroom)
            if useroom and chat:
                if chatroom.id == chat.id:
                    return True
                else:
                    return False            
        except Exception as e:
            return None 
           
    @database_sync_to_async        
    def add_message(self, chatroom, user, content):
        try:
            message = Message.objects.create(
                id = int_id(),
                content = content,
                created_at=datetime.now(),
                user=user,
                chat_room=chatroom
            )
            return message   
        except:
            return None
        
    @database_sync_to_async
    def get_messages(self, chatroom):
        try:
            messages = Message.objects.filter(chat_room = chatroom)
            return messages
        except:
            return None
            
    @database_sync_to_async
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except:
            return None



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            user_id = self.scope['user'].id
            # Agrégate al grupo de canales correspondiente al usuario
            await self.channel_layer.group_add(f"notifications_{user_id}", self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Maneja la desconexión del WebSocket
        print("WebSocket desconectado.")

    async def send_notification(self, event):
        # Envía el mensaje de notificación al cliente conectado
        await self.send(text_data=json.dumps(event))