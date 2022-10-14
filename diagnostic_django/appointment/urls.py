from django.urls import path
from .views import *
from .view_manager import *

urlpatterns = [

    path('book-appointment/', AppointmentAPI.as_view(), name='booking-appointment'),
    path('appointment/<int:id>/', DetailAppointment.as_view(), name='appointment'),
    path('branches/', BranchAPI.as_view(), name="branches"),
    path('branch/<id>/', DetailBranch.as_view(), name="branch"),
    path('labs/', LabAPI.as_view(), name="labs"),
    path('lab/', DetailLab.as_view(), name="lab"),
    path('bills/', BillAPI.as_view(), name="bills"),
    path('bill/<int:id>/', DetailBill.as_view(), name="bill"),
    path('tests/', TestAPI.as_view(), name="tests"),
    path('reviews/', ReviewAPI.as_view(), name="reviews"),
    path('reports/', ReportAPI.as_view(), name="reports"),

    # path('get-employee/', get_employees, name='get-employee'),
    path('get-details-for-booking-appointment/', DetailsForBooking.as_view(), name='get-details-for-booking-appointment')
    # path('get-details-for-booking-appointment/', AppointmentManager.as_view(), name='get-details-for-booking-appointment')
]
