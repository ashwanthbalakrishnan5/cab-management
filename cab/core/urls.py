from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"assignment", views.AssignmentViewSet)
router.register(r"driver", views.DriverProfileViewSet)
router.register(r"car", views.CarProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
