from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('customersignup/', customersignup.as_view(), name="customersignup"),
    path('customerexecutivesignup/', customerexecutivesignup.as_view(), name="customerexecutivesignup"),
    path('salesexecutivesignup/', salesexecutivesignup.as_view(), name="salesexecutivesignup"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]