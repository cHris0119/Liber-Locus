
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import ReviewLike, Review,User
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
                if like:
                    likeus = ReviewLike.objects.get(user=user, review=review)
                    likeus.delete()
                    like = ReviewLike.objects.filter(user=user, review=review).exists()
                    likes = ReviewLike.objects.filter(review=review).count()
                    self.send(text_data=json.dumps({
                        'user_like': like,
                        'likes': likes}))
                else:
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

            except User.DoesNotExist:
        # Handle user not found error
                pass

            except Review.DoesNotExist:
        # Handle review not found error
                pass
