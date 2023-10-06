
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ReviewLike, Review,User

class LikesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.close()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        
        if action == 'like':
            email = data.get('email')
            user = User.objects.get(email = email)
            review_id = data.get('review_id')
            review = Review.objects.get(id = review_id)
            like_exists = ReviewLike.objects.filter(user=user, review=review).exists()
            
            likes = ReviewLike.objects.filter(review=review).count()
            
            await self.send(text_data=json.dumps({'user_like': like_exists, 'likes': likes}))