from django.urls import path, include, re_path
from rest_framework import routers
from LB_API import views_marketPlace as vw
from LB_API import views_login as vl
from rest_framework.authtoken import views
from LB_API import views as v


urlpatterns = [
    path('api/gettoken/', views.obtain_auth_token),
    path('api/obtainUser/<str:token>', vl.obtainUser, name='obtainUser'),
    path('api/login/', vl.loginUser, name='login'),
    path('api/logout/<int:id>', vl.logOut, name='logout'),
    path('api/obtainDirection/<int:user_id>/', vl.obtainDirection, name='obtainDirection'),
    path('api/editDirection/<int:id>', vl.editDirection, name='editDirection'),
    path('api/registerUser/', vl.registerUser, name='registerUser'),
    path('api/editarUser/<int:id>/', vl.editUser, name='editUser'),
    path('api/books/create/', vw.book_create, name='book_create'),  # Ruta para agregar un libro (POST)
    path('api/books/update/<int:pk>/', vw.book_update, name='book_update'),  # Ruta para actualizar un libro por ID (PUT) 
    path('api/books/delete/int:pk>/', vw.book_delete, name='book_delete'),  
    # path('api/books/get/<int:pk>/', vw.book_get, name='book_get') ,
    path('api/communeGet', v.getCommunes, name='communeGet')
    
]
