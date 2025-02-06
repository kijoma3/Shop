from django.shortcuts import render, redirect
from .forms import ProductForm, ProductImageFormSet
from .models import Product, HeaderGallery
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from django.http import JsonResponse

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

def register(request):
    userr = authenticate(username="brandon", password="a")
    nachricht = ""
    if userr is not None:
        nachricht = "Eingeloggt"
    else:
        nachricht = "nicht eingeloggt"
    if(request.method == "POST"):
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")

        user = User.objects.create_user(name, email, password)
        user.save()
    return render(request, 'register.html', {'nachricht': nachricht})


@login_required
def cartView(request):
    cart = json.loads(request.COOKIES.get("cart", "[]"))
    products =[]
    for product in cart:
        products.append(Product.objects.get(id=product))
    return render(request, 'cart.html', {'products': products})
    
def addCartView(request):
    productId = request.GET.get('productId')
    cart = json.loads(request.COOKIES.get('cart', '[]'))
    cart.append(productId)

    response = JsonResponse({"message": "Produkt hinzugefügt", "cart": cart})
    response.set_cookie("cart", json.dumps(cart), max_age=3600 * 24 * 7)
    return response

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerGallery'] = HeaderGallery.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'