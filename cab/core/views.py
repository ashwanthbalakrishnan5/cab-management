from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import DriverProfile, CarProfile, Assignment
from .serializers import (
    DriverProfileSerializer,
    CarProfileSerializer,
    AssignmentSerializer,
)


# Create your views here.
class DriverProfileViewSet(
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    GenericViewSet,
    CreateModelMixin,
):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer

    @action(
        detail=False,
        methods=["get", "post"],
    )
    def me(self, request):
        if request.user.role != "driver":
            return Response({"detail": "You are not a driver"}, status=403)
        if request.method == "POST":
            user = get_user_model().objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "GET":
            driver = get_object_or_404(DriverProfile, user=request.user)
            serializer = self.get_serializer(driver)
            return Response(serializer.data)


class CarProfileViewSet(ModelViewSet):
    queryset = CarProfile.objects.all()
    serializer_class = CarProfileSerializer


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def create(self, request, *args, **kwargs):
        car_id = request.data.get("car")
        driver_id = request.data.get("driver")

        if car_id and driver_id:
            car = get_object_or_404(CarProfile, pk=car_id)
            driver = get_object_or_404(DriverProfile, pk=driver_id)
            if not driver.available:
                return Response(
                    {"error": "The driver is not available for assignment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not car.available:
                return Response(
                    {"error": "The car is not available for assignment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            assignment = Assignment(car=car, driver=driver)
            assignment.save()
            car.available = False
            car.save()
            driver.available = False
            driver.save()
            serializer = AssignmentSerializer(assignment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if car_id:
            car = get_object_or_404(CarProfile, pk=car_id)
            if not car.available:
                return Response(
                    {"error": "The car is not available for assignment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            driver = DriverProfile.objects.filter(available=True).first()
            if driver:
                assignment = Assignment(car=car, driver=driver)
                assignment.save()
                car.available = False
                car.save()
                driver.available = False
                driver.save()
                serializer = AssignmentSerializer(assignment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "No available drivers."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if driver_id:
            driver = get_object_or_404(DriverProfile, pk=driver_id)
            if not driver.available:
                return Response(
                    {"error": "The driver is not available for assignment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            car = CarProfile.objects.filter(available=True).first()
            if car:
                assignment = Assignment(car=car, driver=driver)
                assignment.save()
                car.available = False
                car.save()
                driver.available = False
                driver.save()
                serializer = AssignmentSerializer(assignment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "No available cars."}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"error": "Please provide either car_id or driver_id."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def perform_destroy(self, instance):
        car = instance.car
        driver = instance.driver

        car.available = True
        car.save()
        driver.available = True
        driver.save()

        instance.delete()
