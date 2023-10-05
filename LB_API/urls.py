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
    path('api/obtainUser/<str:token>/', vg.obtainUser, name='obtainUser'),
    path('api/login/', vl.loginUser, name='login'),
    path('api/logout/<int:id>/', vl.logout, name='logout'),
    path('api/obtainDirection/<int:user_id>/', vg.obtainDirection, name='obtainDirection'),
    path('api/editDirection/<int:id>/', vpu.editDirection, name='editDirection'),
    path('api/registerUser/', vl.registerUser, name='registerUser'),
    path('api/editUser/<int:id>/', vpu.editUser, name='editUser'),
    path('api/books/create/', vpo.book_create, name='book_create'),  # Ruta para agregar un libro (POST)
    path('api/books/update/<int:pk>/', vpu.book_update, name='book_update'),  # Ruta para actualizar un libro por ID (PUT) 
    path('api/books/delete/<int:pk>/', vd.book_delete, name='book_delete'),  
    path('api/communeGet/', vg.getCommunes, name='communeGet'),
    path('api/getCategories/', vg.getCategories, name='getCategories'),
    path('api/books/get_all_books/', vg.get_all_books, name='get_all_books'),
    path('api/books/get_user_books/', vg.get_user_books, name='get_user_books'),
    path('api/reviews/create/', vpo.review_create, name='review_create'),
    path('api/getReviews/', vg.getReviews, name='getReviews'),
    path('api/reviews/get_user_reviews/', vg.get_user_reviews, name='get_user_reviews')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)