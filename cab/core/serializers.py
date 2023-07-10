from rest_framework import serializers
from .models import DriverProfile, CarProfile, Assignment


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = "__all__"


class CarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarProfile
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
