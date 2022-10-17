import json

from django.db.models import Q

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


class AppointmentsDetails:

    def get_complete_appointments_data():
        appointments = Appointment.objects.all()
        appointments_tests=[]
        for appointment in appointments:
            each_appointment_tests = list(appointment.tests.all().values(
                'test_id', 'test_name', 'test_description'
            ))
            appointments_tests.append(each_appointment_tests)
        appointments_tests_data = json.dumps(appointments_tests)
        appointments = list(appointments.values(
            'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot',
            'doctor_id__staff_id', 'doctor_id__user_id__username',
            'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
            'lab_technician__user_id__username',
            'sample_collector__staff_id', 'sample_collector__user_id__username', 'status',
        ))
        appointments = json.dumps(appointments)
        return (appointments, appointments_tests_data)
    
    def get_staff_related_appointments_data(staff_id: str, designation: str):
        query = Q()
        if designation == "Doctor":
            query &= Q(doctor_id_id=staff_id)
        elif designation == "Nurse":
            query &= Q(nurse_id_id=staff_id)
        elif designation == "Lab Technician":
            query &= Q(lab_technician_id=staff_id)
        elif designation == "Sample Collector":
            query &= Q(sample_collector_id=staff_id)
        appointments = Appointment.objects.filter(query)
        appointments = list(appointments.values(
            'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot', 'status',
        ))
        appointments = json.dumps(appointments)
        return appointments