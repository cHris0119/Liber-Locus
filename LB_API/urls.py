from django.urls import path, include
from rest_framework import routers
from LB_API import views

router = routers.DefaultRouter()
router.register(r'users', views.userView, 'users')

urlpatterns = [
    path("api/", include(router.urls))
]
