from django.urls import path, include, re_path
from rest_framework import routers
from LB_API import views_marketPlace as vw
from LB_API import views_login as vl
from rest_framework.authtoken import views


urlpatterns = [
    path('api/gettoken/', views.obtain_auth_token),
    path('api/login/', vl.loginUser, name='login'),
    path('api/registerUser/', vl.registerUser, name='registerUser'),
    path('api/editarUser/int:id/', vl.editUser, name='editUser'),
    path('api/books/create/', vw.book_create, name='book_create'),  # Ruta para agregar un libro (POST)
    path('api/books/update/<int:pk>/', vw.book_update, name='book_update')  # Ruta para actualizar un libro por ID (PUT)
]
