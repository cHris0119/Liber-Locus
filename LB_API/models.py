from django.db import models

class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    question_id = models.IntegerField(db_column='QUESTION_id')  # Field name made lowercase.
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ANSWER'


class Auction(models.Model):
    id = models.IntegerField(primary_key=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    duration_days = models.IntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    auction_state_id = models.IntegerField(db_column='AUCTION_STATE_id')  # Field name made lowercase.
    book_id = models.IntegerField(db_column='BOOK_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AUCTION'


class AuctionOffer(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    auction_id = models.IntegerField(db_column='AUCTION_id')  # Field name made lowercase.
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AUCTION_OFFER'


class AuctionState(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=45, db_comment='CANCELED/AVAILABLE/FINISHED')

    class Meta:
        managed = False
        db_table = 'AUCTION_STATE'


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_comment='only positive numbers')
    description = models.CharField(max_length=200)
    author = models.CharField(max_length=45)
    book_img = models.CharField(max_length=255, db_comment='URL')
    seller_id = models.IntegerField()
    book_state_id = models.IntegerField(db_column='BOOK_STATE_id')  # Field name made lowercase.
    valoration = models.IntegerField(blank=True, null=True)
    book_category_id = models.IntegerField(db_column='BOOK_CATEGORY_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BOOK'


class BookCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BOOK_CATEGORY'


class BookState(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=45, db_comment='SOLD/AVAILABLE/IN AUCTION')

    class Meta:
        managed = False
        db_table = 'BOOK_STATE'


class Branch(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    direction = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'BRANCH'


class ChatRoom(models.Model):
    id = models.IntegerField(primary_key=True)
    book_id = models.IntegerField(db_column='BOOK_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CHAT_ROOM'


class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField()
    discussion_id = models.IntegerField(db_column='DISCUSSION_id')  # Field name made lowercase.
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMMENTS'


class Commune(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'COMMUNE'


class Direction(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    calle = models.CharField(max_length=50)
    numero = models.IntegerField()
    commune_id = models.IntegerField(db_column='COMMUNE_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIRECTION'


class Discussion(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    created_by = models.CharField(max_length=45)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    forum_user_id = models.IntegerField(db_column='FORUM_USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DISCUSSION'


class Forum(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    forum_img = models.CharField(max_length=255, blank=True, null=True, db_comment='URL')
    forum_category_id = models.IntegerField(db_column='FORUM_CATEGORY_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FORUM'


class ForumCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FORUM_CATEGORY'


class ForumUser(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    forum_id = models.IntegerField(db_column='FORUM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FORUM_USER'


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    chat_room_id = models.IntegerField(db_column='CHAT_ROOM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MESSAGE'


class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField()
    is_read = models.CharField(max_length=10)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NOTIFICATION'


class PaymentMethod(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, rut) found, that is not supported. The first column is selected. 
    rut = models.CharField(max_length=12)
    method_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.CharField(max_length=4)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PAYMENT_METHOD'
        unique_together = (('id', 'rut'),)


class PostVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    purchase_detail_id = models.IntegerField(db_column='PURCHASE_DETAIL_id')  # Field name made lowercase.
    state_post_venta_id = models.IntegerField(db_column='STATE_POST_VENTA_id')  # Field name made lowercase.
    branch_id = models.IntegerField(db_column='BRANCH_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POST_VENTA'


class PurchaseDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    chat_room_id = models.IntegerField(db_column='CHAT_ROOM_id', blank=True, null=True)  # Field name made lowercase.
    auction_id = models.IntegerField(db_column='AUCTION_id', blank=True, null=True)  # Field name made lowercase.
    purchase_detail_state_id = models.IntegerField(db_column='PURCHASE_DETAIL_STATE_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PURCHASE_DETAIL'


class PurchaseDetailState(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=100, db_comment='CANCELED/IN PROCESS/APPROVED')

    class Meta:
        managed = False
        db_table = 'PURCHASE_DETAIL_STATE'


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    book_id = models.IntegerField(db_column='BOOK_id')  # Field name made lowercase.
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUESTION'


class Refund(models.Model):
    id = models.IntegerField(primary_key=True)
    reason = models.TextField()
    date_refund = models.DateTimeField()
    post_venta_id = models.IntegerField(db_column='POST_VENTA_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REFUND'


class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REPORT'


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    description = models.TextField()
    valoration = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)
    review_img = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    book_id = models.IntegerField(db_column='BOOK_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REVIEW'


class ReviewLike(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    review_id = models.IntegerField(db_column='REVIEW_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REVIEW_LIKE'


class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'ROLE'


class StatePostVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=100, db_comment='ON HOLD: En espera de recibirlo la sucursal\nCANCELED: El libro nunca llego a la sucursal\nCONFIRMED: La sucursal confirmó la llegada del libro\nPAYED: El contador pagó al vendedro')

    class Meta:
        managed = False
        db_table = 'STATE_POST_VENTA'


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SUBSCRIPTION'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    direction_id = models.IntegerField(db_column='DIRECTION_id')  # Field name made lowercase.
    user_photo = models.CharField(max_length=255, blank=True, null=True, db_comment='URL')
    subscription_id = models.IntegerField(db_column='SUBSCRIPTION_id', db_comment='FREE/SUB_1/SUB_2/SUB_3')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER'


class UserRole(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    role_id = models.IntegerField(db_column='ROLE_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROLE'


class UserRoom(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(db_column='USER_id')  # Field name made lowercase.
    chat_room_id = models.IntegerField(db_column='CHAT_ROOM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROOM'