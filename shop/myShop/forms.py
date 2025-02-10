from django import forms
from django.urls import reverse_lazy
from .models import Product, ProductImage, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['titel', 'beschreibung', 'preis']
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['vorname', 'nachname', 'adresse', 'plz', 'ort', 'agb']
        success_url = reverse_lazy('checkout')
        widgets = {
            'vorname': forms.TextInput(attrs={'class': 'form-control'}),
            'nachname': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'plz': forms.NumberInput(attrs={'class': 'form-control'}),
            'ort': forms.TextInput(attrs={'class': 'form-control'}),
            'agb': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'agbCheck'}),
        }

ProductImageFormSet = forms.inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3)
