from django.urls import path
from .views import BranchHandler, RegisterEmployee,RegisterCustomer, loginUser , logoutUser , LoginView ,userView , RefreshToken ,LogoutView


urlpatterns = [
    path('register-customer/' ,RegisterCustomer.as_view(),name='register-customer' ),
    path('register-employee/' ,RegisterEmployee.as_view(),name='register-employee' ),
    path('branch/',BranchHandler.as_view(),name='branch'),
    path('logout/',LogoutView.as_view(), name='logout'),
    # path('login/',LoginView.as_view(),name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', userView, name='user'),
    path('refresh-token/', RefreshToken.as_view(), name='refresh-token'),
]

# chnges done