from django.shortcuts import render, redirect
from .forms import ProductForm, ProductImageFormSet
from .models import Product
from django.views.generic import DetailView, ListView

# Create your views here.
def addProduct(request):
    if request.method == 'POST':
        productForm = ProductForm(request.POST)
        productImagesForm = ProductImageFormSet(request.POST, request.FILES)
        if productForm.is_valid() and productImagesForm.is_valid():
            product = productForm.save()
            images = productImagesForm.save(commit=False)
            for image in images:
                image.produkt = product
                image.save()
            return redirect('index')
    else:
        productForm = ProductForm()
        productImagesForm = ProductImageFormSet()

        return render(request, 'index.html', {'productForm': productForm, 'imageForm': productImagesForm})
    
def startseite(request):
    products = Product.objects.all()
    return render(request, 'productList.html', {'products': products})

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'