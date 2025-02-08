from django.shortcuts import render, redirect

from .forms import ProductForm, ProductImageFormSet, UserProfileForm
from .models import Product, HeaderGallery, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from django.http import JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

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
    preisGesamt = 0
    for productId in cart:
        product = Product.objects.get(id=productId)
        products.append(product)
        preisGesamt += product.preis

    paypal_dict = {
        "business": "sb-xjis637545904@business.example.com",
        "amount": str(preisGesamt),
        "item_name": "Testprodukt",
        "invoice": str(uuid.uuid4()),
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse("product_list")),
        "return_url": request.build_absolute_uri(reverse("payment_done")),
        "cancel_return": request.build_absolute_uri(reverse("product_list")),
        "custom": json.dumps(cart)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'cart.html', {'products': products, 'preisGesamt': preisGesamt, 'paypalForm': form})
    

def editProfile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'editProfile.html', {'form': form})



def addCartView(request):
    productId = request.GET.get('productId')
    cart = json.loads(request.COOKIES.get('cart', '[]'))
    cart.append(productId)

    response = JsonResponse({"message": "Produkt hinzugefügt", "cart": cart})
    response.set_cookie("cart", json.dumps(cart), max_age=3600 * 24 * 7)
    return response

def payment_done(request):
    response = render(request, "payment_done.html")
    response.delete_cookie("cart")
    return response


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerGallery'] = HeaderGallery.objects.all()
        return context
    
    def get_queryset(self):
        return Product.objects.filter(ist_verkauft=False)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'userProfile'

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile