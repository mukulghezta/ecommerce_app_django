from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('createorder/<product_id>/', create_order, name='createorder'),
    path('mycourses/', mycourses, name='mycourses'),
    path('mycoursedetail/<order_id>/', mycoursedetail, name='mycoursedetail'),
    path('cancelorder/<order_id>/', cancel_order, name='cancelorder'),

    path('allorders/', all_orders, name='allorders'),
    path('allcancelledorders/', all_cancelled_orders, name='allcancelledorders'),
    path('detailcancelledorder/<order_id>', detail_cancelled_order, name='detailcancelledorder'),
    path('createcancellationapproval/<order_id>', create_cancellation_approval, name='createcancellationapproval'),

    path('approvalrequestsall/', approval_requests_all, name='approvalrequestsall'),
    path('approvalrequestdetail/<order_id>', approval_request_detail, name='approvalrequestdetail'),
    path('approverequest/<order_id>', approve_request, name='approverequest'),
]