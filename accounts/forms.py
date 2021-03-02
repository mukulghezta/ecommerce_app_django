from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, CustomerExecutive, SalesExecutive
from django.db import transaction


class CustomerSignupForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.username = self.cleaned_data.get('username')
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.email = self.cleaned_data.get('email')
        customer.save()
        return user


class CustomerExecutiveSignupForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_customerexecutive = True
        user.save()
        customerexecutive = CustomerExecutive.objects.create(user=user)
        customerexecutive.username = self.cleaned_data.get('username')
        customerexecutive.first_name = self.cleaned_data.get('first_name')
        customerexecutive.last_name = self.cleaned_data.get('last_name')
        customerexecutive.email = self.cleaned_data.get('email')
        customerexecutive.save()
        return user


class SalesExecutiveSignupForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_salesexecutive = True
        user.save()
        salesrexecutive = SalesExecutive.objects.create(user=user)
        salesrexecutive.username = self.cleaned_data.get('username')
        salesrexecutive.first_name = self.cleaned_data.get('first_name')
        salesrexecutive.last_name = self.cleaned_data.get('last_name')
        salesrexecutive.email = self.cleaned_data.get('email')
        salesrexecutive.save()
        return user

