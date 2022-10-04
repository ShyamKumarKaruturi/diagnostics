from django.urls import path
from .views import *

urlpatterns = [
    path('book-appointment/', AppointmentAPI.as_view(), name='booking-appointment'),
    path('branches/', BranchAPI.as_view(), name="branches"),
    path('labs/', LabAPI.as_view(), name="labs"),
    path('tests/', TestAPI.as_view(), name="tests"),
    path('reviews/', ReviewAPI.as_view(), name="reviews"),
    path('bills/', BillAPI.as_view(), name="bills"),
    path('reports/', ReportAPI.as_view(), name="reports"),
    path('get-employee/', getEmployees, name='get-employee'),
    path('get-employee/', getEmployees, name='get-employee'),
]
