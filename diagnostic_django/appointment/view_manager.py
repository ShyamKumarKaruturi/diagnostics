import json

from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Customer, Staff, User
from users.serializers import EmployeeSerializer
from .models import Branch, Appointment, Lab, Bill, Test, Review, Report
from .serializers import *


class AppointmentManager(APIView):
    @staticmethod
    def get(request):
        try:
            users = list(Customer.objects.all().values(
                'customer_id', 'user_id__id', 'user_id__username'
            ))
            users = json.dumps(users)
            branches = list(Branch.objects.all().values(
                'branch_id', 'branch_name'
            ))
            branches = json.dumps(branches)
            tests = list(Test.objects.all().values(
                'test_id', 'test_name'
            ))
            tests = json.dumps(tests)
            doctors = list(Staff.objects.filter(designation="Doctor").values(
                'staff_id', 'user_id__id', 'user_id__username'
            ))
            doctors = json.dumps(doctors)
            nurses = list(Staff.objects.filter(designation="Nurse").values(
                'staff_id', 'user_id__id', 'user_id__username'
            ))
            nurses = json.dumps(nurses)
            lab_technicians = list(Staff.objects.filter(designation="Lab Technician").values(
                'staff_id', 'user_id__id', 'user_id__username'
            ))
            lab_technicians = json.dumps(lab_technicians)
            sample_collectors = list(Staff.objects.filter(designation="Sample Collector").values(
                'staff_id', 'user_id__id', 'user_id__username'
            ))
            sample_collectors = json.dumps(sample_collectors)
            return Response({
                'users': users, 'branches': branches, 'tests': tests, 'doctors': doctors, 'nurses': nurses,
                'lab_technicians': lab_technicians, 'sample_collectors': sample_collectors
            }, status=200)
        except Exception as error:
            return Response(str(error), status=500)
