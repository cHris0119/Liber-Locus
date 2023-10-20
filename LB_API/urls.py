from django.urls import path
from LB_API import views_login as vl
from rest_framework.authtoken import views
from LB_API import views_post as vpo
from LB_API import views_delete as vd
from LB_API import views_get as vg
from LB_API import views_put as vpu
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/gettoken/', views.obtain_auth_token),
    # Vistas del login
    path('api/login/', vl.loginUser, name='login'),
    path('api/logout/<int:id>/', vl.logout, name='logout'),
    path('api/registerUser/', vl.registerUser, name='registerUser'),
    # Vistas con metodo POST
    path('api/books/create/', vpo.book_create, name='book_create'),  # Ruta para agregar un libro (POST)
    path('api/reviews/create/', vpo.review_create, name='review_create'),
    path('api/reviews/like_a_post/<int:id>/', vpo.like_a_post, name='like_a_post'),
    path('api/create_forum/', vpo.create_forum, name='create_forum'),
    path('api/join_forum/<int:id>/', vpo.join_forum, name='join_forum'),
    path('api/users/follow/<int:idUser>/', vpo.followUser, name='follow_user'),
    path('api/user/send_mail/<str:email>/', vpo.send_email, name='send_mail'), 
    path('api/user/send_mail/<str:email>', vpo.send_email),
    path('api/create_discussion/', vpo.create_discussion, name='create_discussion'),
    #Vistas con metodo DELETE
    path('api/books/delete/<int:pk>/', vd.book_delete, name='book_delete'), 
    path('api/reviews/delete/<int:pk>/', vd.review_delete, name='review_delete'),
    path('api/forums/delete/<int:pk>/', vd.delete_forum, name='delete_forum'),
    path('api/forums/leave_forum/<int:forum_id>/', vd.leave_forum, name='leave_forum'),
    path('api/discussions/delete/<int:discussion_id>/', vd.delete_discussion, name='delete_discussion'),
    # Vistas con metodo GET
    path('api/obtainUser/<str:token>/', vg.obtainUser, name='obtainUser'),
    path('api/obtainDirection/<int:user_id>/', vg.obtainDirection, name='obtainDirection'),
    path('api/communeGet/', vg.getCommunes, name='communeGet'),
    path('api/getCategories/', vg.getCategories, name='getCategories'),
    path('api/books/get_all_books/', vg.get_all_books, name='get_all_books'),
    path('api/books/get_user_books/', vg.get_user_books, name='get_user_books'),
    path('api/getReviews/', vg.getReviews, name='getReviews'),
    path('api/reviews/get_user_reviews/', vg.get_user_reviews, name='get_user_reviews'),
    path('api/reviews/reviews_likes/<int:id>/', vg.reviews_likes, name='review_likes'),
    path('api/forums/get_all_forums/', vg.get_all_forums, name='get_all_forums'),# Te da todos los foros 
    path('api/forums/get_user_forums/<int:user_id>/', vg.get_user_forums, name='get_user_forums'), # Te da todos los foros en los que se encuentra 1 usuario en especifico
    path('api/forums/category/<int:category_id>/', vg.get_forums_by_category, name='get_forums_by_category'),
    path('api/get_forum_categories/', vg.get_forum_categories, name='get_forum_categories'),
    path('api/forums/get_forum_users/', vg.get_forum_users, name='get_forum_users'), # Esta vista te da a todos los usuarios que se han unido a algun foro dandote el id de forum_user, el id del usuario y el id del foro
    path('api/forums/get_users_one_forum/<int:forum_id>/', vg.get_users_one_forum, name='get_users_one_forum'), # Este te da a todos los usuarios dentro de 1 foro
    path('api/users/get_all_follow/', vg.get_Follows_followers, name='get_all_follow'),
    path('api/forums/get_forum_discussions/<int:forum_id>/', vg.get_forum_discussions, name='get_forum_discussions'),
    path('api/users/confirm_email/<str:token>/', vg.confirm_email, name='confirm_email'),
    # Vistas con metodo PUT
    path('api/editDirection/<int:id>/', vpu.editDirection, name='editDirection'),
    path('api/editUser/<int:id>/', vpu.editUser, name='editUser'),
    path('api/books/update/<int:pk>/', vpu.book_update, name='book_update'),  # Ruta para actualizar un libro por ID (PUT) 
    path('api/reviews/update/<int:pk>/', vpu.review_update, name='review_update'),
    path('api/forums/update/<int:pk>/', vpu.update_forum, name='update_forum')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)