import json

from .models import *
from .serializers import *


class AppointmentManager:
    def get_appointments_related_all_tests(self, appointments=[]):
        appointments_tests = []
        for appointment in appointments:
            each_appointment_tests = appointment.tests.all().values(
                'test_id', 'test_type', 'test_name'
            )
            serializer = TestSerializer(each_appointment_tests, many=True)
            appointments_tests.append(json.dumps(serializer.data))
        return appointments_tests