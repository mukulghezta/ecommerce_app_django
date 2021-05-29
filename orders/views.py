from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from products.models import Product
from accounts.models import User, Customer, CustomerExecutive, SalesExecutive
from orders.models import Order, CancelledOrder, CancelledApproval, Email, Discount, GST
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import os
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


# CUSTOMER ACTIONS
# For customer to buy a course
@login_required(login_url="/accounts/login/")
def create_order(request, product_id):
    product = Product.objects.get(product_id=product_id)
    logged_in_user = get_object_or_404(Customer, username=str(request.user))
    email = Email.objects.get(email_id=1)
    gst = GST.objects.get(id=1)

    if request.method == "POST":
        obj = Order()
        obj.order_id
        obj.user = logged_in_user
        obj.course = product
        obj.amount = product.product_price
        obj.gst_amount = product.product_price * gst.gst
        obj.final_amount = obj.amount + obj.gst_amount
        obj.order_date
        obj.save()

        template = get_template('orders/orderplaced.html')
        data = {
        "order_id": str(obj.order_id),
        "user": obj.user,
        "course": obj.course,
        "order_date":datetime.now().date(),
        "amount": obj.amount,
        "gst": obj.gst_amount,
        "final_amount": obj.final_amount
        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = 'Invoice_' + data['order_id'] + '.pdf'
        template = get_template('orders/orderplaced.html')


        # Email for order placement
        email = EmailMessage(
            email.email_subject,
            email.email_body.format(obj.user, obj.order_id, obj.course, datetime.now().date()),
            email.email_sender,
            [obj.user.email, 'test@test.com'])
        email.attach(filename, pdf, 'application/pdf')
        email.send()


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
    logged_in_user = get_object_or_404(Customer, username=str(request.user))
    cancelledorder = CancelledOrder.objects.filter(order_id=order_id)
    return render(request, 'orders/customers/mycoursedetail.html', {'course':course, 'cancelledorder':cancelledorder, 'logged_in_user':logged_in_user})

# For customer to cancel an order/course
@login_required(login_url="/accounts/login/")
def cancel_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    cancelled_order_id = order.order_id
    logged_in_user = get_object_or_404(Customer, username=str(request.user))
    email = Email.objects.get(email_id=2)
    customer_executive = CustomerExecutive.objects.get(username="user02")

    if request.method == "POST":
        obj = CancelledOrder()
        obj.order_id = order
        obj.user = logged_in_user
        obj.amount = order.amount
        obj.gst_amount = order.gst_amount
        obj.final_amount = order.final_amount
        obj.order_date = order.order_date
        obj.save()

        # Email to customer executive for order cancellation notification
        send_mail(
            email.email_subject,
            email.email_body.format(order.order_id, order.course.product_name, order.order_date.date(), datetime.now().date()),
            email.email_sender,
            [customer_executive.email, 'test@test.com'],
        )
        messages.info(request, "Order sent for Cancellation approval!!!")
        return redirect('orders:mycourses')
    return render(request, 'orders/customers/cancelorder.html', {'order':order})

######################################################################################################

# CUSTOMER EXECUTIVE ACTIONS

@login_required(login_url="/accounts/login/")
def all_orders(request):
    orders = Order.objects.all()
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_customerexecutive:
        return render(request, 'orders/customerexecutives/allorders.html', {'orders':orders})
    else:
        return HttpResponse('Unauthorized', status=401)


# For customer executive to view all cancelled orders
@login_required(login_url="/accounts/login/")
def all_cancelled_orders(request):
    orders = CancelledOrder.objects.all()
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_customerexecutive:
        return render(request, 'orders/customerexecutives/allcancelledorders.html', {'orders':orders})
    else:
        return HttpResponse('Unauthorized', status=401)

# For customer executive to view the details of a cancelled order
@login_required(login_url="/accounts/login/")
def detail_cancelled_order(request, order_id):
    order = CancelledOrder.objects.get(order_id=order_id)
    app_req = CancelledApproval.objects.filter(order_id=order_id)
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_customerexecutive:
        return render(request, 'orders/customerexecutives/detailcancelledorder.html', {'order':order, 'app_req':app_req})
    else:
        return HttpResponse('Unauthorized', status=401)

# For customer executive to send the cancellation request to sales executive for approval
@login_required(login_url="/accounts/login/")
def create_cancellation_approval(request, order_id):
    cancelledorder = CancelledOrder.objects.get(order_id=order_id)
    order = Order.objects.get(order_id=order_id)
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_customerexecutive:
        if request.method == "POST":
            obj = CancelledApproval()
            obj.order_id = cancelledorder
            obj.user = cancelledorder.user
            obj.amount = order.amount     
            obj.gst_amount = order.gst_amount     
            obj.final_amount = order.final_amount
            obj.order_date = order.order_date
            obj.cancelled_order_date = cancelledorder.cancelled_order_date

            # Calculating difference between order date and cancellation date
            i = order.order_date
            j = cancelledorder.cancelled_order_date
            k = j-i
            no_of_days = k.days
            if no_of_days == 0:
                no_of_days = 1
            obj.date_diff = no_of_days

            # if no_of_days <= 7:
            #     obj.refund_amount = order.amount
            # elif no_of_days>7 and no_of_days<=15:
            #     obj.refund_amount = order.amount/2

            # discount_record = Discount.objects.get(no_of_days>discount_start and no_of_days<discount_end)

            if no_of_days < 16:
                amount = order.final_amount - order.gst_amount
                dis = Discount.objects.get(discount_start__lte=no_of_days, discount_end__gte=no_of_days)
                obj.refund_amount = amount * dis.discount_percent
            else:
                obj.refund_amount = 0

            obj.save()
            messages.info(request, "Request sent to Sales Executive for cancellation approval!!!")
            return redirect('orders:allcancelledorders')
        return render(request, 'orders/customerexecutives/createcancellationapproval.html', {'cancelledorder':cancelledorder, 'order':order })
    else:
        return HttpResponse('Unauthorized', status=401)

######################################################################################################

# SALES EXECUTIVE ACTIONS
# For sales executive to view approval requests
@login_required(login_url="/accounts/login/")
def approval_requests_all(request):
    app_req = CancelledApproval.objects.all()
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_salesexecutive:
        return render(request, 'orders/salesexecutives/approvalrequestsall.html', {'app_req':app_req})
    else:
        return HttpResponse('Unauthorized', status=401)

# For sales executive to view the details of an approval request
@login_required(login_url="/accounts/login/")
def approval_request_detail(request, order_id):
    app_req = CancelledApproval.objects.get(order_id=order_id)
    days =  app_req.date_diff
    logged_in_user = get_object_or_404(User, username=str(request.user))
    if logged_in_user.is_salesexecutive:
        return render(request, 'orders/salesexecutives/approvalrequestdetail.html', {'app_req':app_req,'days':days})
    else:
        return HttpResponse('Unauthorized', status=401)
    
# For generating pdf invoice
# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def generate_pdf(request, *args, **kwargs):
#     template = get_template('orders/invoice.html')
#     context = {
#         "order_id": "order_id",
#         "user": "user",
#         "amount":"amount",
#         "order_date":"order_date",
#         "cancelled_order_date":"cancelled_order_date"
#     }
#     html = template.render(context)
#     pdf = render_to_pdf('orders/invoice.html', context)
#     if pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "Invoice_%s.pdf" %("12341231")
#         return
#     return pdf

# For sales executive to approve the request
@login_required(login_url="/accounts/login/")
def approve_request(request, order_id):
    app_req = CancelledApproval.objects.get(order_id=order_id)
    can_req = CancelledOrder.objects.get(order_id=order_id)
    ord_req = Order.objects.get(order_id=order_id)

    emailapp = Email.objects.get(email_id=3)
    emailrej = Email.objects.get(email_id=4)


    if request.POST.get('approve'):

        template = get_template('orders/cancellationapproval.html')
        data = {
        "order_id": str(ord_req.order_id),
        "user": ord_req.user.username,
        "order_date":app_req.order_date,
        "cancelled_order_date":app_req.cancelled_order_date,
        "course_price":app_req.amount,
        "order_amount":app_req.final_amount,
        "refund_amount":app_req.refund_amount,
        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = 'Invoice_' + data['order_id'] + '.pdf'
        template = get_template('orders/cancellationapproval.html')

        # Email to customer for order cancellation approval
        email = EmailMessage(
            emailapp.email_subject,
            emailapp.email_body.format(ord_req.user.username, ord_req.course.product_name, ord_req.order_id, app_req.refund_amount),
            emailapp.email_sender,
            [app_req.user.email, 'test@test.com'])
        email.attach(filename, pdf, 'application/pdf')
        email.send()

        app_req.delete()
        can_req.delete()
        ord_req.delete()
        messages.info(request, "Order cancellation approved!!! Customer has been notified via email.")
        return redirect('orders:approvalrequestsall')
        

    if request.POST.get('reject'):

        template = get_template('orders/cancellationrejection.html')
        data = {
        "order_id": str(ord_req.order_id),
        "user": ord_req.user.username,
        "order_date":app_req.order_date,
        "cancelled_order_date":app_req.cancelled_order_date,
        "amount":app_req.amount,
        "refund_amount":app_req.refund_amount,
        }
        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = result.getvalue()
        filename = 'Invoice_' + data['order_id'] + '.pdf'
        template = get_template('orders/cancellationrejection.html')

        # Email to customer for order cancellation rejection
        email = EmailMessage(
        emailrej.email_subject,
        emailrej.email_body.format(ord_req.user.username, ord_req.course.product_name, ord_req.order_id,app_req.refund_amount),
        emailrej.email_sender,
        [app_req.user.email, 'test@test.com'])
        email.attach(filename, pdf, 'application/pdf')
        email.send()

        app_req.delete()
        can_req.delete()
        ord_req.delete()
        messages.info(request, "Order cancellation rejected!!! Customer has been notified via email.")
        return redirect('orders:approvalrequestsall')

    return redirect('orders:approvalrequestsall')
    



