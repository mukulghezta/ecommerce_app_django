from django.contrib import admin
from .models import User, Customer, CustomerExecutive, SalesExecutive

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(CustomerExecutive)
admin.site.register(SalesExecutive) 