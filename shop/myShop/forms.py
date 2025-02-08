from django import forms
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

ProductImageFormSet = forms.inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3)
