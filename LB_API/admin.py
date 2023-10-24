from django.contrib import admin
from .models import *
from django.contrib.auth.models import User as AdminUser

# Register your models here.
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Role)
admin.site.register(Answer)
admin.site.register(Auction)
admin.site.register(AuctionOffer)
admin.site.register(AuctionState)
admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookState)
admin.site.register(Branch)
admin.site.register(ChatRoom)
admin.site.register(Comments)
admin.site.register(Commune)
admin.site.register(Direction)
admin.site.register(Discussion)
admin.site.register(Forum)
admin.site.register(ForumCategory)
admin.site.register(ForumUser)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(PaymentMethod)
admin.site.register(PostVenta)
admin.site.register(PurchaseDetail)
admin.site.register(PurchaseDetailState)
admin.site.register(Refund)
admin.site.register(Report)
admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(StatePostVenta)
admin.site.register(Subscription)
admin.site.register(Question)


