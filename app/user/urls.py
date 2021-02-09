from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views


router = DefaultRouter()
router.register(r'passengers', views.PassengerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
