from django import forms

from market.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =['title', 'description', 'price_cost', 'price_sale']