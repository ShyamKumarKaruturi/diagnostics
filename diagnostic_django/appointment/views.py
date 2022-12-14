import json

from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .view_manager import AppointmentManager
from users.models import Customer, Staff, User
from users.serializers import EmployeeSerializer
from .models import *
from .serializers import *


# @csrf_exempt
# class AppointmentBooking(APIView):
#     def get(self, request, id=""):
#         if id == "":
#             appointments = Appointment.objects.all()
#             serializer = AppointmentSerializer(appointments, many=True)
#         else:
#             appointment = Appointment.objects.get(appointment_id=id)
#             serializer = AppointmentSerializer(appointment, many=False)
#         return Response(json.dumps(serializer.data), status=200)
#
#     def post(self, request):
#         print(request.data)
#         data = request.data.get('form')
#         username = request.data.get('username')
#         print(username)
#         user = User.objects.get(username=username)
#         print(user)
#         customer = Customer.objects.get(user_id=user.id)
#         print(customer)
#         data['user'] = customer.customer_id
#         print(data)
#         apmt = AppointmentSerializer(data=data)
#         print(apmt)
#         if apmt.is_valid():
#             apmt.save()
#             return Response({"message": "appointment_booked"}, status=200)
#         else:
#             return Response({"message": "appointment not booked"}, status=200)
#         # return Response({"message":"appointment not booked"} , status = 200 )
#
#     def delete(self,request):
#         pass

class AppointmentAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                appointments = Appointment.objects.all()
                appointments_tests = []
                for appointment in appointments:
                    each_appointment_tests = appointment.tests.all().values(
                        'test_id', 'test_type', 'test_name', 'test_description'
                    )
                    serializer = TestSerializer(each_appointment_tests, many=True)
                    appointments_tests.append(json.dumps(serializer.data))
                # appointments_tests = AppointmentManager.get_appointments_related_all_tests(list(appointments))
                appointments = appointments.values(
                    'appointment_id', 'user__customer_id', 'user__user_id__username', 'date', 'slot',
                    'doctor_id__staff_id', 'doctor_id__user_id__username',
                    'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
                    'lab_technician__user_id__username',
                    'sample_collector__staff_id', 'sample_collector__user_id__username', 'status'
                )

                serializer = AppointmentSerializer(appointments, many=True)
            else:
                appointment = Appointment.objects.get(appointment_id=id)
                serializer = AppointmentSerializer(appointment, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response({'appointments': json.dumps(serializer.data), 'related_tests': appointments_tests}, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        username = request.data.get('username')
        # username = request.data['username']
        print(username)
        user = User.objects.get(username=username)
        print(user)
        customer = Customer.objects.get(user_id=user.id)
        print(customer)
        data['user'] = customer.customer_id
        data['branch'] = None
        data['doctor_id'] = None
        data['nurse_id'] = None
        data['lab_technician'] = None
        data['sample_collector'] = None
        print(data)
        apmt = AppointmentSerializer(data=data)
        print(apmt)
        if apmt.is_valid():
            apmt.save()
            return Response({"message": "appointment_booked"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        appointment_data = JSONParser().parse(request)
        appointment = Appointment.objects.get(appointment_id=appointment_data['id'])
        serializer = AppointmentSerializer(appointment, data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        appointment = Appointment.objects.get(appointment_id=id)
        if appointment:
            appointment.delete()
            return JsonResponse(data={'success': 'Appointment Data deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Appointment Doesn\'t exists . So, Appointment Data cound not be deleted successfully.'},
            safe=False)


class BranchAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                branches = Branch.objects.all()
                serializer = BranchSerializer(branches, many=True)
            else:
                branch = Branch.objects.get(appointment_id=id)
                serializer = BranchSerializer(branch, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = BranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Branch Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        branch = Branch.objects.get(branch_id=data['id'])
        serializer = BranchSerializer(branch, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        branch = Branch.objects.get(branch_id=id)
        if branch:
            branch.delete()
            return JsonResponse(data={'success': 'Branch deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Branch doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


class LabAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                labs = Lab.objects.all()
                serializer = LabSerializer(labs, many=True)
            else:
                lab = Lab.objects.get(appointment_id=id)
                serializer = LabSerializer(lab, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = LabSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Branch Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        lab = Lab.objects.get(lab_id=data['id'])
        serializer = LabSerializer(lab, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        lab = Lab.objects.get(lab_id=id)
        if lab:
            lab.delete()
            return JsonResponse(data={'success': 'Branch deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Branch doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


class TestAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                tests = Test.objects.all()
                serializer = LabSerializer(tests, many=True)
            else:
                test = Test.objects.get(test_id=id)
                serializer = TestSerializer(test, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        lab = data['lab']
        data['lab'] = None
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = TestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Test Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        test = Test.objects.get(test_id=data['id'])
        serializer = TestSerializer(test, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        test = Test.objects.get(lab_id=id)
        if test:
            test.delete()
            return JsonResponse(data={'success': 'Test deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Test doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


class ReviewAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                reviews = Review.objects.all()
                serializer = ReviewSerializer(reviews, many=True)
            else:
                review = Review.objects.get(test_id=id)
                serializer = ReviewSerializer(review, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Test Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        review = Review.objects.get(id=data['id'])
        serializer = ReviewSerializer(review, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        review = Review.objects.get(lab_id=id)
        if review:
            review.delete()
            return JsonResponse(data={'success': 'Test deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Test doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


class BillAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                bills = Bill.objects.all()
                serializer = BillSerializer(bills, many=True)
            else:
                bill = Bill.objects.get(id=id)
                serializer = BillSerializer(bill, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = BillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Test Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        bill = Bill.objects.get(id=data['id'])
        serializer = BillSerializer(bill, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        bill = Bill.objects.get(lab_id=id)
        if bill:
            bill.delete()
            return JsonResponse(data={'success': 'Test deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Test doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


class ReportAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            if id == "":
                reports = Report.objects.all()
                serializer = ReportSerializer(reports, many=True)
            else:
                report = Report.objects.get(id=id)
                serializer = ReportSerializer(report, many=False)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        # data = request.data
        # username = request.data.get('username')
        # username = request.data['username']
        print(data)
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Test Created"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )

    @staticmethod
    def put(request):
        # branch_data = JSONParser().parse(request)
        data = request.data.get('form')
        report = Report.objects.get(id=data['id'])
        serializer = ReportSerializer(report, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    @staticmethod
    def delete(request, id=""):
        report = Report.objects.get(lab_id=id)
        if report:
            report.delete()
            return JsonResponse(data={'success': 'Test deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Test doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)


@api_view(['GET'])
def getEmployees(request):
    if request.GET['role'] == 'doctor':
        doctors = Staff.objects.filter(designation="Doctor")
        serializer = EmployeeSerializer(doctors, many=True)
        return Response(serializer.data, status=200)
    if request.GET['role'] == 'nurse':
        doctors = Staff.objects.filter(designation="Nurse")
        serializer = EmployeeSerializer(doctors, many=True)
        return Response(serializer.data, status=200)
    if request.GET['role'] == 'lab':
        doctors = Staff.objects.filter(designation="Lab Technician")
        serializer = EmployeeSerializer(doctors, many=True)
        return Response(serializer.data, status=200)
    if request.GET['role'] == 'sample':
        doctors = Staff.objects.filter(designation="Sample Collector")
        serializer = EmployeeSerializer(doctors, many=True)
        return Response(serializer.data, status=200)
    return Response({"message": "not working"}, status=200)
