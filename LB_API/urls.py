from django.urls import path, include
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
    path('registerUser/', vl.registerUser, name='registerUser')
]
