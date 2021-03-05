from django.contrib import admin
from .models import Order, CancelledOrder, CancelledApproval, Email, Discount

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'course', 'amount', 'order_date']

admin.site.register(Order, OrderAdmin)


class CancelledOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'amount', 'order_date', 'cancelled_order_date']

admin.site.register(CancelledOrder, CancelledOrderAdmin)


class CancelledApprovalAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'amount', 'order_date', 'cancelled_order_date', 'date_diff', 'refund_amount']

admin.site.register(CancelledApproval, CancelledApprovalAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ['email_id', 'email_type', 'email_subject', 'email_body', 'email_sender', 'email_recipients']

admin.site.register(Email, EmailAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount_id', 'discount_start', 'discount_end', 'discount_percent']

admin.site.register(Discount, DiscountAdmin)
