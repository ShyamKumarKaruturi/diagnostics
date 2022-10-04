from django.urls import path
from .views import *

urlpatterns = [
    path('book-appointment/', AppointmentAPI.as_view(), name='booking-appointment'),
<<<<<<< HEAD
=======
    path('branches/', BranchAPI.as_view(), name="branches"),
    path('labs/', LabAPI.as_view(), name="labs"),
    path('tests/', TestAPI.as_view(), name="tests"),
    path('reviews/', ReviewAPI.as_view(), name="reviews"),
    path('bills/', BillAPI.as_view(), name="bills"),
    path('reports/', ReportAPI.as_view(), name="reports"),
    path('get-employee/', getEmployees, name='get-employee'),
>>>>>>> 009931820fb739c57844ef550e19b0b1a4439052

    path('get-employee/', getEmployees, name='get-employee'),
]
