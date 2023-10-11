
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review,User

class LikesConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
    def disconnect(self, close_code):
        self.close()
    
    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        
        if action == 'like':
            id = data.get('id')
            user = User.objects.get(id = id)
            review_id = data.get('review_id')
            review = Review.objects.get(id = review_id)
            like_exists = ReviewLike.objects.filter(user=user, review=review).exists()
            
            likes = ReviewLike.objects.filter(review=review).count()
            
            self.send(text_data=json.dumps({'user_like': like_exists, 'likes': likes}))