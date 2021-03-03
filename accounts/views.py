from django.shortcuts import render, redirect
from .models import User
from .forms import CustomerSignupForm, CustomerExecutiveSignupForm, SalesExecutiveSignupForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm

# Renders page with different signup options 
def signup_view(request):
    return render(request, 'accounts/signup.html')

# Signup form for customers
class customersignup(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = 'accounts/customersignup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('products:home')

# Signup form for customer executives
class customerexecutivesignup(CreateView):
    model = User
    form_class = CustomerExecutiveSignupForm
    template_name = 'accounts/customerexecutivesignup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('products:home')

# Signup form for sale executives
class salesexecutivesignup(CreateView):
    model = User
    form_class = SalesExecutiveSignupForm
    template_name = 'accounts/salesexecutivesignup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('products:home')

# For all users to login 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request, user)
                return redirect('products:home')
            else:
                return redirect('products:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

# For all users to logout
def logout_view(request):
    logout(request)
    return redirect('products:home')
