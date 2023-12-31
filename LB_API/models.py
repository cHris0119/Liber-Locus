from django.db import models


class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='QUESTION_id')  # Field name made lowercase.
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ANSWER'


class Auction(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, AUCTION_STATE_id) found, that is not supported. The first column is selected.
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    duration_days = models.IntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    auction_state = models.ForeignKey('AuctionState', on_delete=models.CASCADE, db_column='AUCTION_STATE_id')  # Field name made 
    book = models.ForeignKey('Book', on_delete=models.CASCADE, db_column='BOOK_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AUCTION'
        unique_together = (('id', 'auction_state'),)


class AuctionOffer(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, db_column='AUCTION_id')  # Field name made lowercase.
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

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
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, BOOK_STATE_id, BOOK_CATEGORY_id) found, that is not supported. The first column is selected.
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_comment='only positive numbers')
    description = models.CharField(max_length=200)
    author = models.CharField(max_length=45)
    book_img = models.ImageField(upload_to='books',max_length=255, db_comment='URL')
    seller = models.ForeignKey('User', on_delete=models.CASCADE)
    book_state = models.ForeignKey('BookState', on_delete=models.CASCADE, db_column='BOOK_STATE_id')  # Field name made lowercase.
    created_at = models.DateTimeField()
    book_category = models.ForeignKey('BookCategory', on_delete=models.CASCADE, db_column='BOOK_CATEGORY_id')  # Field name made

    class Meta:
        managed = False
        db_table = 'BOOK'
        unique_together = (('id', 'book_state', 'book_category'),)


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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='BOOK_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CHAT_ROOM'


class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField()
    discussion = models.ForeignKey('Discussion', on_delete=models.CASCADE, db_column='DISCUSSION_id')  # Field name made lowercase.
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

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
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, db_column='COMMUNE_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DIRECTION'


class Discussion(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    created_by = models.CharField(max_length=45)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    forum_user = models.ForeignKey('ForumUser', on_delete=models.CASCADE, db_column='FORUM_USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DISCUSSION'


class Follow(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    followed = models.ForeignKey('Followed', on_delete=models.CASCADE, db_column='FOLLOWED_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FOLLOW'


class Followed(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FOLLOWED'


class Forum(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, FORUM_CATEGORY_id) found, that is not supported. The first column is selected.
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    forum_img = models.ImageField(upload_to='forums',max_length=255, blank=True, null=True, db_comment='URL')
    forum_category = models.ForeignKey('ForumCategory', on_delete=models.CASCADE, db_column='FORUM_CATEGORY_id')  # Field name made lowercase.
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'FORUM'
        unique_together = (('id', 'forum_category'),)


class ForumCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FORUM_CATEGORY'


class ForumUser(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, db_column='FORUM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FORUM_USER'


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_column='CHAT_ROOM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MESSAGE'


class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField()
    is_read = models.CharField(max_length=10)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

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
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PAYMENT_METHOD'
        unique_together = (('id', 'rut'),)


class PostVenta(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, STATE_POST_VENTA_id, BRANCH_id) found, that is not supported. The first column is selected.
    purchase_detail = models.ForeignKey('PurchaseDetail', on_delete=models.CASCADE, db_column='PURCHASE_DETAIL_id')  # Field name made lowercase.
    state_post_venta = models.ForeignKey('StatePostVenta', on_delete=models.CASCADE, db_column='STATE_POST_VENTA_id')  # Field name made lowercase.
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='BRANCH_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POST_VENTA'
        unique_together = (('id', 'state_post_venta', 'branch'),)


class PurchaseDetail(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, PURCHASE_DETAIL_STATE_id) found, that is 
    purchase_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_column='CHAT_ROOM_id')  # Field name made lowercase.
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, db_column='AUCTION_id', blank=True, null=True)  # Field name made lowercase.
    purchase_detail_state = models.ForeignKey('PurchaseDetailState', on_delete=models.CASCADE, db_column='PURCHASE_DETAIL_STATE_id')  # Field name made lowercase.
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='BOOK_id', blank=True, null=True)  # Field name made lowercase.
    code_verify = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'PURCHASE_DETAIL'
        unique_together = (('id', 'purchase_detail_state'),)


class PurchaseDetailState(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=100, db_comment='CANCELED/IN PROCESS/APPROVED')

    class Meta:
        managed = False
        db_table = 'PURCHASE_DETAIL_STATE'


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='BOOK_id')  # Field name made lowercase.
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUESTION'


class Refund(models.Model):
    id = models.IntegerField(primary_key=True)
    reason = models.TextField()
    date_refund = models.DateTimeField()
    post_venta = models.ForeignKey(PostVenta, on_delete=models.CASCADE, db_column='POST_VENTA_id')  # Field name made lowercase.
    post_venta_state_post_venta_id = models.IntegerField(db_column='POST_VENTA_STATE_POST_VENTA_id')  # Field name made lowercase.
    post_venta_branch_id = models.IntegerField(db_column='POST_VENTA_BRANCH_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REFUND'


class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REPORT'


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    description = models.TextField()
    valoration = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)
    review_img = models.ImageField(upload_to='reviews',max_length=255, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REVIEW'


class ReviewLike(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_column='REVIEW_id')  # Field name made lowercase.

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
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, SUBSCRIPTION_id) found, that is not supported. The first column is selected.
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    user_photo = models.ImageField(upload_to='user',max_length=255, blank=True, null=True, db_comment='URL')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, db_column='SUBSCRIPTION_id', db_comment='FREE/SUB_1/SUB_2/SUB_3')  # Field name made lowercase.
    is_active = models.BooleanField(blank=True, null=True)
    confirm_key = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'USER'
        unique_together = (('id', 'subscription'),)


class UserRole(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, USER_id, ROLE_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='ROLE_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROLE'
        unique_together = (('id', 'user', 'role'),)


class UserRoom(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_id')  # Field name made lowercase.
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_column='CHAT_ROOM_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROOM'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey('AuthPermission', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'