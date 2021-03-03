from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from accounts.models import Customer
from orders.models import Order, CancelledOrder, CancelledApproval
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


# CUSTOMER ACTIONS
# For customer to buy a course
@login_required(login_url="/accounts/login/")
def create_order(request, product_id):
    product = Product.objects.get(product_id=product_id)
    logged_in_user = get_object_or_404(Customer, username=str(request.user))

    if request.method == "POST":
        obj = Order()
        obj.user = logged_in_user
        obj.course = product
        obj.amount = product.product_price
        obj.save()
        messages.info(request,"Course Ordered!!!")
        return redirect('products:home')
    return render(request, 'orders/customers/createorder.html', {'product':product})

# For customer to view the courses he has bought
@login_required(login_url="/accounts/login/")
def mycourses(request):
    logged_in_user = get_object_or_404(Customer, username=str(request.user))
    courses = Order.objects.filter(user=logged_in_user)
    return render(request, 'orders/customers/mycourses.html', {'courses':courses})

# For customer to view the details of a course
@login_required(login_url="/accounts/login/")
def mycoursedetail(request, order_id):
    course = Order.objects.get(order_id=order_id)
    cancelledorder = CancelledOrder.objects.filter(order_id=order_id)
    return render(request, 'orders/customers/mycoursedetail.html', {'course':course, 'cancelledorder':cancelledorder})

# For customer to cancel an order/course
@login_required(login_url="/accounts/login/")
def cancel_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    cancelled_order_id = order.order_id
    logged_in_user = get_object_or_404(Customer, username=str(request.user))

    if request.method == "POST":
        obj = CancelledOrder()
        obj.order_id = order
        obj.user = logged_in_user
        obj.amount = order.amount
        obj.order_date = order.order_date

        obj.save()
        messages.info(request, "Order sent for Cancellation approval!!!")
        return redirect('orders:mycourses')
    return render(request, 'orders/customers/cancelorder.html', {'order':order})

######################################################################################################

# CUSTOMER EXECUTIVE ACTIONS
# For customer executive to view all cancelled orders
@login_required(login_url="/accounts/login/")
def all_cancelled_orders(request):
    orders = CancelledOrder.objects.all()
    return render(request, 'orders/customerexecutives/allcancelledorders.html', {'orders':orders})

# For customer executive to view the details of a cancelled order
@login_required(login_url="/accounts/login/")
def detail_cancelled_order(request, order_id):
    order = CancelledOrder.objects.get(order_id=order_id)
    app_req = CancelledApproval.objects.filter(order_id=order_id)
    return render(request, 'orders/customerexecutives/detailcancelledorder.html', {'order':order, 'app_req':app_req})

# For customer executive to send the cancellation request to sales executive for approval
@login_required(login_url="/accounts/login/")
def create_cancellation_approval(request, order_id):
    cancelledorder = CancelledOrder.objects.get(order_id=order_id)
    order = Order.objects.get(order_id=order_id)

    if request.method == "POST":
        obj = CancelledApproval()
        obj.order_id = cancelledorder
        obj.user = cancelledorder.user
        obj.amount = cancelledorder.amount     
        obj.order_date = cancelledorder.order_date
        obj.cancelled_order_date = cancelledorder.cancelled_order_date
            
        # Calculating difference between order date and cancellation date
        i = order.order_date
        j = cancelledorder.cancelled_order_date
        k = j-i
        no_of_days = k.days
        obj.date_diff = no_of_days
        
        if no_of_days <= 7:
            obj.refund_amount = order.amount
        elif no_of_days>7 and no_of_days<=15:
            obj.refund_amount = order.amount/2
            
        obj.save()
        messages.info(request, "Request sent to Sales Executive for cancellation approval!!!")
        return redirect('orders:allcancelledorders')
    return render(request, 'orders/customerexecutives/createcancellationapproval.html', {'cancelledorder':cancelledorder })

######################################################################################################

# SALES EXECUTIVE ACTIONS
# For sales executive to view approval requests
@login_required(login_url="/accounts/login/")
def approval_requests_all(request):
    app_req = CancelledApproval.objects.all()
    return render(request, 'orders/salesexecutives/approvalrequestsall.html', {'app_req':app_req})

# For sales executive to view the details of an approval request
@login_required(login_url="/accounts/login/")
def approval_request_detail(request, order_id):
    app_req = CancelledApproval.objects.get(order_id=order_id)
    days =  app_req.date_diff
    return render(request, 'orders/salesexecutives/approvalrequestdetail.html', {'app_req':app_req,'days':days})

#For sales executive to approve the request
@login_required(login_url="/accounts/login/")
def approve_request(request, order_id):
    app_req = CancelledApproval.objects.get(order_id=order_id)
    can_req = CancelledOrder.objects.get(order_id=order_id)
    ord_req = Order.objects.get(order_id=order_id)

    if request.method == "POST":
        app_req.delete()
        can_req.delete()
        ord_req.delete()
        messages.info(request, "Order cancellation approved!!!")
        return redirect('orders:approvalrequestsall')
    return redirect('orders:approvalrequestsall')



