from rest_framework import serializers
from . import models


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lab
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ['test_id', 'test_type', 'test_name', 'test_description']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ['user', 'slot', 'doctor_id', 'nurse_id', 'lab_technician', 'sample_collector', 'status']


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = "__all__"
