from django.contrib import admin
from .models import Order, CancelledOrder, CancelledApproval

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'course', 'amount', 'order_date']

admin.site.register(Order, OrderAdmin)


class CancelledOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'amount', 'order_date', 'cancelled_order_date']

admin.site.register(CancelledOrder, CancelledOrderAdmin)


class CancelledApprovalAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'amount', 'order_date', 'cancelled_order_date', 'date_diff']

admin.site.register(CancelledApproval, CancelledApprovalAdmin)