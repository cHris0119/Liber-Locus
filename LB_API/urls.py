from django.urls import path, include, re_path
from rest_framework import routers
from LB_API import views as vw
from LB_API import views_login as vl
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'users', vw.userView, 'users')

urlpatterns = [
    path("api/", include(router.urls)),
    path('gettoken/', views.obtain_auth_token),
    path('login/', vl.loginUser, name='login'),
    path('registerUser/', vl.registerUser, name='registerUser'),
    path('api/books/create/', views.book_create, name='book_create'),  # Ruta para agregar un libro
    re_path(r'^api/books/update/(?P<pk>\d+)/$', views.book_update, name='book_update')  # Ruta para actualizar un libro por ID
]
