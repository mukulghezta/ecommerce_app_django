from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<product_id>/', productdetail, name='productdetail'),
    path('productcreate/', productcreate, name='productcreate'),
    path('productedit/<product_id>/', productedit, name='productedit'),
    path('productdelete/<product_id>/', productdelete, name='productdelete'),
]