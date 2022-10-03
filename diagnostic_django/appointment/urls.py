from django.urls import path
from .views import *

urlpatterns = [
    path('booking-appointment/', AppointmentAPI.as_view(), name='booking-appointment'),
    path('get-employee/', getEmployees, name='get-employee'),

]
