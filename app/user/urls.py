from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views


router = DefaultRouter()
router.register(r'passengers', views.PassengerViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'admins', views.AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
