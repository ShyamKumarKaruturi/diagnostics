import json

from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# from .view_manager import AppointmentManager
from users.models import Customer, Staff, User
from users.serializers import EmployeeSerializer
from .models import Branch, Appointment, Lab, Bill, Test, Review, Report
from .serializers import *
from django.db.models import Q

class DetailsForBooking(APIView):
    @staticmethod
    def get(request):
        doctors = Staff.objects.filter(designation = 'Doctor')
        doctors = list(doctors.values("staff_id" , "user_id__username"))
        nurses= Staff.objects.filter(designation='Nurse')
        nurses = list(nurses.values("staff_id", "user_id__username"))
        lab_technicians = Staff.objects.filter(designation='Lab Technician')
        lab_technicians = list(lab_technicians.values("staff_id", "user_id__username"))
        sample_collectors = Staff.objects.filter(designation='Sample Collector')
        sample_collectors = list(sample_collectors.values("staff_id", "user_id__username"))
        tests = Test.objects.all()
        tests = TestSerializer(tests,many=True)
        branches = Branch.objects.all()
        branches = BranchSerializer(branches, many=True)
        users = Customer.objects.all()
        users = list(users.values('customer_id','user_id__username'))

        return Response({'doctors':json.dumps(doctors) , 'nurses':json.dumps(nurses),'lab_technicians':json.dumps(lab_technicians),
                       'sample_collectors':json.dumps(sample_collectors) , 'tests':tests.data , 'branches':branches.data,
                         'users':json.dumps(users)} ,status=200)


class DetailAppointment(APIView):
    @staticmethod
    def get(request,id):
        appointment = Appointment.objects.get(appointment_id=id)
        appointments_tests = list(appointment.tests.all().values(
                        'test_id', 'test_name', 'test_description'
                    ))
        serializer = AppointmentSerializer(appointment, many=False)
        # appointment = appointment.values(
        #     'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot',
        #     'doctor_id__staff_id', 'doctor_id__user_id__username',
        #     'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
        #     'lab_technician__user_id__username',
        #     'sample_collector__staff_id', 'sample_collector__user_id__username', 'status',
        # )
        return Response({'appointment': serializer.data, 'related_tests': appointments_tests},
                        status=200)

    @staticmethod
    def delete(request, id):
        appointment = Appointment.objects.filter(appointment_id=id).first()
        if appointment:
            appointment.delete()
            return JsonResponse(data={'success': 'Appointment Data deleted successfully.'}, safe=False)
        else:
            return JsonResponse(data={'success': 'Appointment Data is not deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Appointment Doesn\'t exists . So, Appointment Data cound not be deleted successfully.'},
            safe=False)

    @staticmethod
    def put(request,id):
        appointment_data = JSONParser().parse(request)
        appointment = Appointment.objects.get(appointment_id=id)
        serializer = AppointmentSerializer(appointment, data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class FilterAppointment(APIView):
    def get(self,request):
        text = request.GET['text']
        appointments = Appointment.objects.filter(Q(user__user_id__username__icontains=text) | Q(user__customer_id__icontains=text))
        appointments_tests = []
        for appointment in appointments:
            each_appointment_tests = list(appointment.tests.all().values(
                'test_id', 'test_name', 'test_description'
            ))
            # serializer = TestSerializer(each_appointment_tests, many=True)
            appointments_tests.append(each_appointment_tests)
        appointments_tests_data = json.dumps(appointments_tests)
        appointments = list(appointments.values(
            'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot',
            'doctor_id__staff_id', 'doctor_id__user_id__username',
            'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
            'lab_technician__user_id__username',
            'sample_collector__staff_id', 'sample_collector__user_id__username', 'status',
        ))
        # serializer = AppointmentSerializer(appointments, many=True)
        return Response({'appointments': json.dumps(appointments), 'related_tests': appointments_tests_data},
                        status=200)

class AppointmentAPI(APIView):
    @staticmethod
    def get(request):
        appointments = Appointment.objects.all()
        appointments_tests = []
        for appointment in appointments:
            each_appointment_tests = list(appointment.tests.all().values(
                'test_id', 'test_name', 'test_description'
            ))
            # serializer = TestSerializer(each_appointment_tests, many=True)
            appointments_tests.append(each_appointment_tests)
        appointments_tests_data = json.dumps(appointments_tests)
        appointments = list(appointments.values(
            'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot',
            'doctor_id__staff_id', 'doctor_id__user_id__username',
            'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
            'lab_technician__user_id__username',
            'sample_collector__staff_id', 'sample_collector__user_id__username', 'status',
        ))
        # serializer = AppointmentSerializer(appointments, many=True)
        return Response({'appointments': json.dumps(appointments), 'related_tests': appointments_tests_data},
                    status=200)
    # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        print(data)
        apmt = AppointmentSerializer(data=data)
        if apmt.is_valid():
            apmt.save()
            return Response({"message": "appointment_booked"}, status=200)
        else:
            return Response({"message": "appointment not booked"}, status=500)
        # return Response({"message":"appointment not booked"} , status = 200 )


class CustomerAppointments(APIView):
    def get(self,request,cust_id):
        appointments = Appointment.objects.filter(user__customer_id = cust_id)
        appointments_tests = []
        for appointment in appointments:
            each_appointment_tests = list(appointment.tests.all().values(
                'test_id', 'test_name', 'test_description'
            ))
            # serializer = TestSerializer(each_appointment_tests, many=True)
            appointments_tests.append(each_appointment_tests)
        appointments_tests_data = json.dumps(appointments_tests)
        appointments = list(appointments.values(
            'appointment_id', 'user__customer_id', 'user__user_id__username', 'slot',
            'doctor_id__staff_id', 'doctor_id__user_id__username',
            'nurse_id__staff_id', 'nurse_id__user_id__username', 'lab_technician__staff_id',
            'lab_technician__user_id__username',
            'sample_collector__staff_id', 'sample_collector__user_id__username', 'status',
        ))
        # serializer = AppointmentSerializer(appointments, many=True)
        return Response({'appointments': json.dumps(appointments), 'related_tests': appointments_tests_data},
                        status=200)


class DetailBranch(APIView):
    @staticmethod
    def get(request, id):
        branch = Branch.objects.get(branch_id=id)
        serializer = BranchSerializer(branch, many=False)
        return Response({'branch': serializer.data},status=200)
    @staticmethod
    def delete(request, id):
        branch = Branch.objects.get(branch_id=id)
        if branch:
            branch.delete()
            return JsonResponse(data={'success': 'Branch deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Branch doesn\'t exists . So, Branch could not be deleted successfully.'},
            safe=False)
    @staticmethod
    def put(request,id):
        data = request.data.get('form')
        branch = Branch.objects.get(branch_id=id)
        serializer = BranchSerializer(branch, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Branch Created", "action_status": "success"}, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class BranchAPI(APIView):
    @staticmethod
    def get(request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        branch_id = data['branch_id']
        # branch = Branch.objects.filter(branch_id= branch_id).first()
        # if branch:
        #     return Response({"message": "Branch Already exist", "action_status": "failure"}, status=200)
        serializer = BranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Branch Created", "action_status": "success"}, status=200)
        else:
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            return Response({"message":error_list,"action_status": "failure"}, status=200)


class DetailLab(APIView):
    pass


class LabAPI(APIView):
    @staticmethod
    def get(request):
        labs = list(Lab.objects.all().values(
            'lab_id', 'lab_name', 'branch__branch_id',
            'branch__branch_name'
        ))
        return Response({'labs':json.dumps(labs)}, status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        serializer = LabSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Lab Created" , "action_status": "success"}, status=200)
        else:
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            return Response({"message": error_list, "action_status": "failure"}, status=200)
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

        tests = list(Test.objects.all().values(
            'test_id', 'test_type', 'test_name', 'test_description', 'lab__lab_id', 'lab__lab_name'
        ))
        # serializer = LabSerializer(tests, many=True)
        return Response(json.dumps(tests), status=200)
        # return Response(json.dumps(serializer.data), status=200)

    @staticmethod
    def post(request):
        print(request.data)
        data = request.data.get('form')
        test_id = data['test_id']
        try:
            test = Test.objects.get(test_id=test_id)
            return Response({"message": "Test Already exist" , "action_status": "failure"}, status=200)
        except:
            print(data)
            serializer = TestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "New Test Created", "action_status": "success"}, status=200)
            else:
                return Response({"message": "there is some issure, please try again later", "action_status": "failure"}, status=500)
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
        reviews = list(Review.objects.all().values(
            'id', 'user_id__username', 'rating', 'comment'
        ))
        # serializer = ReviewSerializer(reviews, many=True)
        return Response(json.dumps(reviews), status=200)
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


class DetailBill(APIView):
    @staticmethod
    def delete(request,id):
        bill = Bill.objects.get(id=id)
        if bill:
            bill.delete()
            return JsonResponse(data={'success': 'Bill Details deleted successfully.'}, safe=False)
        return JsonResponse(
            data={'Failure': 'Bill Doesn\'t exists . So, Bill Data cound not be deleted successfully.'},
            safe=False)

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
    def get(request,id):
        try:
            bill = list(Bill.objects.get(id = id).values(
                'id', 'appointment__appointment_id', 'appointment__user__user_id__username',
                'consultation_fee', 'test_fee', 'tax', 'total'
            ))
            # serializer = BillSerializer(bills, many=True)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(json.dumps(bill), status=200)
        # return Response(json.dumps(serializer.data), status=200)


class BillAPI(APIView):
    @staticmethod
    def get(request):
        try:
            bills = list(Bill.objects.all().values(
                'id', 'appointment__appointment_id', 'appointment__user__user_id__username',
                'consultation_fee', 'test_fee', 'tax', 'total'
            ))
            # serializer = BillSerializer(bills, many=True)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(json.dumps(bills), status=200)
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




class ReportAPI(APIView):
    @staticmethod
    def get(request, id=""):
        try:
            reports = list(Report.objects.all().values(
                'id', 'appointment__appointment_id', 'appointment__user__username',
                'description', 'report_type'
            ))
            # serializer = ReportSerializer(reports, many=True)
        except Exception as error:
            return Response(str(error), status=500)
        return Response(json.dumps(reports), status=200)
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
