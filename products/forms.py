from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_price']