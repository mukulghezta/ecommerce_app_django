from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import CreateProductForm
from accounts.models import SalesExecutive


# Display all products on the home page
def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products':products})

def productdetail(request, product_id):
    product = Product.objects.get(product_id=product_id)
    return render(request, 'products/productdetail.html', {'product':product})

def productcreate(request):
    logged_in_user = get_object_or_404(SalesExecutive, username=str(request.user))
    if request.method == "POST":
        form = CreateProductForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product_seller = logged_in_user
            instance.save()
            return redirect('products:home')
    else:
        form = CreateProductForm()
    return render(request, 'products/productcreate.html', {'form':form})
