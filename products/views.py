from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import CreateProductForm
from accounts.models import SalesExecutive
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Display all products on the home page
def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products':products})

# Display the details of a course to everyone
@login_required(login_url="/accounts/login/")
def productdetail(request, product_id):
    product = Product.objects.get(product_id=product_id)
    return render(request, 'products/productdetail.html', {'product':product})

# For sales executive to add a new course
@login_required(login_url="/accounts/login/")
def productcreate(request):
    logged_in_user = get_object_or_404(SalesExecutive, username=str(request.user))
    if request.method == "POST":
        form = CreateProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product_seller = logged_in_user
            instance.save()
            messages.info(request,"Course added successfully!!!")
            return redirect('products:home')
    else:
        form = CreateProductForm()
    return render(request, 'products/productcreate.html', {'form':form})

# For sales executive to edit his course
# @login_required(login_url="/accounts/login/")
# def productedit(request, product_id):
#     product = Product.objects.get(product_id=product_id)
#     form = CreateProductForm(instance=product)

#     if request.method == "POST":
#         form = CreateProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.info(request,"Course updated successfully!!!")
#             return redirect('products:home')
#     return render(request, 'products/productcreate.html', {'form':form})

# For sales executive to delete his course
def productdelete(request, product_id):
    product = Product.objects.get(product_id=product_id)

    if request.method == "POST":
        product.delete()
        return redirect('products:home')
    return render(request, 'products/productdelete.html', {'product':product})


