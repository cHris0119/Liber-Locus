from django.urls import path
from LB_API import views_login as vl
from rest_framework.authtoken import views
from LB_API import views_post as vpo
from LB_API import views_delete as vd
from LB_API import views_get as vg
from LB_API import views_put as vpu
from LB_API import transbank_view as tv
from LB_API import count_views as count_v
from LB_API import mobile_views as mv
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/gettoken/', views.obtain_auth_token), # Obtener token del usuario
    # Vistas del login
    path('api/login/', vl.loginUser, name='login'), # Iniciar sesion
    path('api/logout/<int:id>/', vl.logout, name='logout'), # deslogearse
    path('api/registerUser/', vl.registerUser, name='registerUser'), # registrar usuario
    # Vistas con metodo POST
    path('api/books/create/', vpo.book_create, name='book_create'),  # Ruta para agregar un libro (POST)
    path('api/reviews/create/', vpo.review_create, name='review_create'), # crear una reseña
    path('api/reviews/like_a_post/<int:id>/', vpo.like_a_post, name='like_a_post'), # dar like a una reseña
    path('api/create_forum/', vpo.create_forum, name='create_forum'), # Crear foro
    path('api/join_forum/<int:id>/', vpo.join_forum, name='join_forum'), # Entrar a un foro
    path('api/users/follow/<int:idUser>/', vpo.followUser, name='follow_user'), # Seguir a un usuario
    path('api/user/send_mail/<str:email>/', vpo.send_email, name='send_mail'), # email para verificar cuenta
    path('api/create_discussion/', vpo.create_discussion, name='create_discussion'), # crear discusion
    path('api/discussion/<int:discussion_id>/add_comment/', vpo.add_comment, name='add_comment'), # agregar comentario a un hilo
    path('api/question/create/<int:bookID>/', vpo.askQuestion, name='askQuestion'), # crear una pregunta en el libro
    path('api/answer/create/<int:Q_id>/', vpo.createAnswer, name='createAnswer'), # crear respuesta en un libro
    path('api/create_subasta/<book_id>/', vpo.create_subasta, name='create_subasta'), # crear subasta
    path('api/subastas/<int:subasta_id>/realizar_puja/', vpo.realizar_puja, name='realizar_puja'), # Realizar puja en subasta
    path('api/finalizar_subasta/<int:subasta_id>/', vpo.finalizar_subasta, name='finalizar_subasta'), # Finalizacion de subasta 
    #Vistas con metodo DELETE
    path('api/books/delete/<int:pk>/', vd.book_delete, name='book_delete'),  # eliminar un libro
    path('api/reviews/delete/<int:pk>/', vd.review_delete, name='review_delete'), # eliminar una reseña
    path('api/forums/delete/<int:pk>/', vd.delete_forum, name='delete_forum'), # eliminar un foro
    path('api/forums/leave_forum/<int:forum_id>/', vd.leave_forum, name='leave_forum'), # salirse de un foro
    path('api/discussions/delete/<int:discussion_id>/', vd.delete_discussion, name='delete_discussion'), # eliminar un hilo
    path('api/forums/<int:forum_id>/remove_user/<int:user_id>/', vd.remove_user_from_forum, name='remove_user_from_forum'), #forum_id= id del foro, owner=quien creo el foro, user id= usuario a eliminar
    path('api/questions/delete/<int:Q_id>/', vd.QuestionDelete, name='QuestionDelete'), # eliminar una pregunta
    path('api/subastas/<int:subasta_id>/cancel/', vd.cancel_subasta, name='cancel_subasta'), # Cancelar subasta
    # Vistas con metodo GET
    path('api/obtainUser/<str:token>/', vg.obtainUser, name='obtainUser'), # otbtener al ususario mediante el token
    path('api/obtainDirection/<int:user_id>/', vg.obtainDirection, name='obtainDirection'), # obtener la direccion
    path('api/communeGet/', vg.getCommunes, name='communeGet'), # obtener las comunas
    path('api/getCategories/', vg.getCategories, name='getCategories'), # obtener las categorias
    path('api/getSubscriptions/', vg.getSubcriptions, name='getSubscription'),
    path('api/books/get_all_books/', vg.get_all_books, name='get_all_books'), # obtener todos los libros
    path('api/books/get_user_books/', vg.get_user_books, name='get_user_books'), # obtener los libros de los usuarios
    path('api/getReviews/', vg.getReviews, name='getReviews'), # obtener una reseña
    path('api/reviews/get_user_reviews/', vg.get_user_reviews, name='get_user_reviews'), # obtener las reseñas de un usuario
    path('api/reviews/reviews_likes/<int:id>/', vg.reviews_likes, name='review_likes'), # obtener likes de una reseña
    path('api/forums/get_all_forums/', vg.get_all_forums, name='get_all_forums'),# Te da todos los foros 
    path('api/forums/get_user_forums/<int:user_id>/', vg.get_user_forums, name='get_user_forums'), # Te da todos los foros en los que se encuentra 1 usuario en especifico
    path('api/forums/category/<int:category_id>/', vg.get_forums_by_category, name='get_forums_by_category'), # te trae los foros por categoria
    path('api/get_forum_categories/', vg.get_forum_categories, name='get_forum_categories'), #  te trae la categoria de los foros
    path('api/forums/get_forum_users/', vg.get_forum_users, name='get_forum_users'), # Esta vista te da a todos los usuarios que se han unido a algun foro dandote el id de forum_user, el id del usuario y el id del foro
    path('api/forums/get_users_one_forum/<int:forum_id>/', vg.get_users_one_forum, name='get_users_one_forum'), # Este te da a todos los usuarios dentro de 1 foro
    path('api/users/get_all_follow/', vg.get_Follows_followers, name='get_all_follow'), # obtener los seguidores de los usuario
    path('api/forums/get_forum_discussions/<int:forum_id>/', vg.get_forum_discussions, name='get_forum_discussions'), # obtener hilos de los foros 
    path('api/users/confirm_email/<str:token>/', vg.confirm_email, name='confirm_email'), # confirmar email del usuario
    path('api/get_user_forum_discussions/<int:forum_id>/', vg.get_user_forum_discussions, name='get_user_forum_discussions'), # Obtener las hilos creadas por 1 usuario dentro del foro
    path('api/questions/getBookQuestions/<int:bookID>/', vg.BookQuestion, name='bookQuestion'), # obtener preguntas del libro
    path('api/latest_discussions/<int:user_id>/', vg.latest_discussions, name='latest_discussions'), # obtener las ultimas discuciones que fueron publicadas en los foros en donde esta el usuario
    path('api/discussions/<int:discussion_id>/', vg.get_discussion_by_id, name='get_discussion_by_id'), # Obtener discusiones/hilos por el ID
    path('api/discussions/<int:discussion_id>/comments/', vg.get_comments, name='get_comments'), #Obtener todos los comentarios dentro de un hilo/discusion
    path('media/<path:path>', vg.getimage, name='getimage'),
    path('api/mis_compras/', vg.get_my_purchases, name='get_my_purchases'), #Obtener las compras del individuo
    path('api/mis_ventas/', vg.get_my_sales, name='get_my_sales'), #Obtener las ventas del individuo
    path('api/auction/get_all_auctions/', vg.get_all_auctions, name='get_all_auctions'), # obtener todos los libros
    path('api/chatroom/get_msg/<int:chat_id>/', vg.get_messages_chatroom, name='get_messages_chat'),
    path('api/forums/get_popular_forums/', vg.get_popular_forums, name='get_popular_forums'),
    path('api/notifications/get_user_notifications/<int:user_id>/', vg.get_user_notifications, name='get_user_notifications'),
    path('api/chatroom/book_data/<int:chat_id>', vg.get_chatroom_books, name='get_chatroom_books'),
    # Vistas con metodo PUT
    path('api/editDirection/<int:id>/', vpu.editDirection, name='editDirection'), # editar direccion
    path('api/editUser/<int:id>/', vpu.editUser, name='editUser'), # editar usuario
    path('api/books/update/<int:pk>/', vpu.book_update, name='book_update'),  # Ruta para actualizar un libro por ID (PUT) 
    path('api/reviews/update/<int:pk>/', vpu.review_update, name='review_update'), # editar reseña
    path('api/forums/update/<int:pk>/', vpu.update_forum, name='update_forum'), # editar foro
    # Url de transbank
    path('api/transbank/iniciar_pago', tv.iniciar_pago, name='iniciar_pago'),
    path('api/transbank/iniciar_pago_suscripcion/', tv.iniciar_pago_suscripcion, name='iniciar_pago_suscripcion'),
    path('api/transbank/retorno_suscripcion/', tv.retorno_pago_suscripcion, name='retorno_pago_suscripcion'),
    path('api/transbank/retorno/', tv.retorno_pago, name='retorno'),
    # Url de contador
    path('api/counter/get_all_sales', count_v.get_all_sales, name='get_all_sales'),
    path('api/transbank/iniciar_pago_contador/', count_v.iniciar_pago_contador, name='iniciar_pago_contador'),
    path('api/transbank/retorno_contador/', count_v.retorno_pago_contador, name='retorno_contador'),
    # Url de la app
    path('api/app/confirm_key/<int:id>/', mv.productReceived, name="confirm_key")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   