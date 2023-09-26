from django.urls import path, include
from rest_framework import routers
from LB_API import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.userView, 'users')

urlpatterns = [
    path("api/", include(router.urls)),
    path('gettoken/', obtain_auth_token)
]
