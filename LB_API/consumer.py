
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review,User
from time import time
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
        
    def disconnect(self):
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
            if like_exists:
                likes = ReviewLike.objects.filter(review=review).count()
            
                self.send(text_data=json.dumps({'user_like': like_exists, 'likes': likes}))
            else:
                ReviewLike.objects.create(
                    id = int_id(),
                    user = user,
                    review = review
                )
                like_exists = ReviewLike.objects.filter(user=user, review=review).exists()
                self.send(text_data=json.dumps({'user_like': like_exists, 'likes': likes}))