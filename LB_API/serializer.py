from rest_framework import serializers
from .models import *


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class roleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: Role
        fields = '__all__'
        
class userRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: UserRole
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'

class AuctionOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionOffer
        fields = '__all__'

class AuctionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionState
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookState
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = '__all__'

class ForumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumUser
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class PostVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVenta
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class PurchaseDetailStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetailState
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'

class StatePostVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatePostVenta
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthtokenToken
        fields = '__all__'
        
class editUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_photo']
        
class editDirectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Direction
        fields = ['calle', 'numero', 'commune']