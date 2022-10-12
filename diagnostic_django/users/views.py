# import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from appointment import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.authentication import get_authorization_header
from  rest_framework import exceptions
# jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from .authentication import create_access_token,create_refresh_token , decode_access_token,decode_refresh_token
from users.serializers import UserSerializer, CustomerSerializer, EmployeeSerializer
from .models import User, Customer, Staff
from appointment.models import Branch
from appointment.serializers import BranchSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout



# @api_view(['POST','PUT'])
# def registerCustomer(request):
#     if request.method == 'POST':
#         print(request.data)
#         print(request)
#         # data = json.parse(request)

#         serializer = UserSerializer(data = request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             customer_obj = CustomerSerializer(data = {"customer_id":"MEDC"+str(user.id),"user_id":user.id})
#             if customer_obj.is_valid():
#                 customer_obj.save()

#             return Response(serializer.data)
#         # print(user_obj)
#         # print(serializer)
#     return Response({"msg":"not created"},status =400)


class RegisterCustomer(APIView):
    def post(self, request):
        print(request.data)
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            print(user)
            return Response({'message': "User  Exist"})
        except:
            data = request.data
            data['user_type'] = 'customer'
            serializer = UserSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                user = serializer.save()
                customer_obj = CustomerSerializer(data={"customer_id": "MEDC" + str(user.id), "user_id": user.id})
                if customer_obj.is_valid():
                    customer_obj.save()
                    return Response({'data': serializer.data, 'message': "registered"}, status=200)
                else:
                    print('invalid')
                    return Response(customer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('invalid')
                return Response({'message': "invalid"})

    def get(self, request):
        users = Customer.objects.all()
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data, status=200)


class RegisterEmployee(APIView):
    def post(self, request):
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
            print(user)
            return Response({'message': "User Exist"})
        except:
            serializer = UserSerializer(
                data={'username': request.data["username"], "first_name": request.data["first_name"],
                      'last_name': request.data["last_name"], 'email': request.data['email'],
                      "mobile_number": request.data["mobile_number"], "age": int(request.data['age']),
                      'address': request.data['address'], "pincode": request.data['pincode'],
                      "password": request.data['password'], "user_type": 'staff'})
            print(serializer)
            if serializer.is_valid():
                user = serializer.save()
                employee_obj = EmployeeSerializer(data={"staff_id": "MEDS" + str(user.id), "user_id": user.id,
                                                        "designation": request.data["designation"],
                                                        "qualification": request.data['qualification'],
                                                        "salary": int(request.data['salary']),
                                                        "years_of_experience": int(request.data[
                                                                                   'years_of_experience']) or 0,
                                                        'branch': request.data['branch']})
                print(employee_obj)
                if employee_obj.is_valid():
                    employee_obj.save()
                    return Response({'data': serializer.data, 'message': "registered"}, status=200)
                else:
                    return Response({'message': "not valid"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('invalid')
                return Response({'message': "not valid"})

    def get(self, request):
        users = Customer.objects.all()
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data, status=200)


class BranchHandler(APIView):
    def get(self, request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=200)


@csrf_exempt
@api_view(['POST'])
def loginUser(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            return Response({'msg': "User Does not Exist"})
        # user = User.objects.get(username=username)
        # if not user:
        #     raise APIException("invalid credentials")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = Customer.objects.filter(user_id=user)
            if len(user_data)==0:
                user_data = Staff.objects.filter(user_id=user)[0]
                print(user_data)
                user_data = EmployeeSerializer(instance=user_data, many=False)
            else:
                user_data = user_data[0]
                user_data = CustomerSerializer(instance=user_data, many=False)
            user = UserSerializer(instance=user, many=False)
            return Response({'msg': "logged in", 'user': user.data, 'user_data': user_data.data}, status=200)
        else:
            return Response({'msg': "password incorrect"})

    return Response({"msg": "not created"}, status=200)


@csrf_exempt
@api_view(['POST'])
def logoutUser(request):
    username = request.data.get("username")
    user = User.objects.get(username=username)
    logout(request)
    return Response({"message": "logged out", 'user': user.username}, status=200)


class LoginView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get('password')
        user = User.objects.filter(username=request.data['username']).first()
        if not user:
            return Response({"message": "user does not exist"}, status=200)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'message': "incorrect password"}, status=200)
        else:
            if user.user_type == 'customer':
                user_type_obj = Customer.objects.filter(user_id = user.id).first()
                user_type_id = user_type_obj.customer_id
            elif user.user_type == 'staff':
                user_type_obj = Staff.objects.filter(user_id=user.id).first()
                user_type_id = user_type_obj.staff_id
            else:
                user_type_id = user.id


        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        print(refresh_token)
        response = Response()

        response.set_cookie(key='refreshToken' , value= refresh_token , httponly = True) # refresh token in cookie n access token in response data
        response.data = {
            'message':"success",
            'token':access_token,
            'user_type' : user.user_type,
            'username' : user.username,
            'user_type_id':user_type_id
        }
        return response

        # return Response({"message": "logged out", 'user': user.username}, status=200)

@csrf_exempt
@api_view(['GET'])
def userView(request):
    auth = get_authorization_header(request).split()   # first param is bearer n 2nd is token (access token)
    if auth and len(auth)==2:
        token = auth[1].decode('utf-8')
        id = decode_access_token(token)
        user = User.objects.filter(id = id).first()
        if user.user_type == 'customer':
            user_type_obj = Customer.objects.filter(user_id=user.id).first()
            user_type_id = user_type_obj.customer_id
        elif user.user_type == 'staff':
            user_type_obj = Staff.objects.filter(user_id=user.id).first()
            user_type_id = user_type_obj.staff_id
        else:
            user_type_id = user.id
        return Response({
            'user_type' : user.user_type,
            'username' : user.username,
            'user_type_id':user_type_id
        })
    raise exceptions.AuthenticationFailed('unauthenticate')


# def userView(request):
#     auth = get_authorization_header(request).split()   # first param is bearer n 2nd is token (access token)
#     if auth and len(auth)==2:
#         token = auth[1].decode('utf-8')
#         id = decode_access_token(token)
#         user = User.objects.filter(id = id).first()
#         return Response(UserSerializer(user).data)
#     raise exceptions.AuthenticationFailed('unauthenticate')

class RefreshToken(APIView):
    authentication_classes = []
    def post(self,request):
        refresh_token  = request.COOKIES.get('refreshToken')
        print(refresh_token)
        id = decode_refresh_token(refresh_token)
        print(id)
        access_token = create_access_token(id)
        print(access_token)
        return Response({
            'token' : access_token
        })


class LogoutView(APIView):
    def post(self,_):
        response = Response()
        response.delete_cookie(key= 'refreshToken')
        response.data = {
            'message' : 'success'
        }
        return response
