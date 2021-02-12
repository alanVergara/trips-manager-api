from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trip import views


router = DefaultRouter()
router.register(r'routes', views.RouterViewSet)
router.register(r'buses', views.BusViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'tickets', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
