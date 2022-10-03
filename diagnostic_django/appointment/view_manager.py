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

        # required_tests = []
        # all_tests = list(Test.objects.all())
        # if len(test_ids != 0):
        #     for test_id in test_ids:
        #         for test in all_tests:
        #             if test['test_id'] == test_id:
        #                 required_tests.append(test.values('test_id', 'test_name', 'test_name'))
        #     serializer = TestSerializer(required_tests, many=True)
        #     return json.dumps(serializer.data)
        # else:
        #     return []

    # if request.method == 'GET':
    #     chefs = Chef.objects.all().values(
    #         'chef_id','user__username', 'user__first_name', 'user__last_name',
    #         'rating', 'number_of_ratings', 'salary', 'manager__user__username',
    #     )
    #     chef_serializer = ChefSerializer(chefs, many=True)
    #     chef_data = json.dumps(chef_serializer.data)
    #     return JsonResponse(chef_data, safe=False)
