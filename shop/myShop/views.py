import os
from django.conf import settings
from django.shortcuts import render, redirect

from shop.settings import VERSAND, WEBHOOK_SECRET

from .forms import ProductForm, ProductImageFormSet, UserProfileForm
from .models import Orders, Product, HeaderGallery, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from django.http import HttpResponseRedirect, JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from paypal.standard.ipn.views import ipn
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
import stripe
import markdown

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


@csrf_exempt   
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



@csrf_exempt
@login_required
def cartView(request):
    cart = json.loads(request.COOKIES.get("cart", "[]"))
    products =[]
    preisGesamt = 0
    userId = request.user.id
    paypalCustom = {}
    paypalCustom['userId'] = userId
    paypalCustom['cart'] = cart
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
        "notify_url": "https://d9b7-145-254-36-25.ngrok-free.app/paypal/ipn/",
        "return_url": request.build_absolute_uri(reverse("payment_done")),
        "cancel_return": request.build_absolute_uri(reverse("product_list")),
        "custom": json.dumps(paypalCustom)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'cart.html', {'products': products, 'preisGesamt': preisGesamt, 'paypalForm': form})
    
@csrf_exempt
def paypal_ipn_exempt(request):
    return ipn(request)


def editProfile(request):
    profile = request.user.userprofile
    next_url = request.GET.get('next', 'profile')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse(next_url))

    else:
        form = UserProfileForm(instance=profile)

    def get_success_url(self):
        next_url = self.request.GET.get('next', reverse('login'))
        return next_url


    return render(request, 'editProfile.html', {'form': form})



def removeItemFromCart(request):
    productId = request.GET.get('productId')
    print("productID: ", productId)
    cart = json.loads(request.COOKIES.get('cart'))
    print("cart: ", cart)

    cart.remove(productId)
    print("cartNew: ", cart)

    response = JsonResponse({"message": "Produkt gelöscht", "cart": cart})
    response.set_cookie("cart", json.dumps(cart), max_age=3600 * 24 * 7)
    return response


def addCartView(request):
    productId = request.GET.get('productId')
    cart = json.loads(request.COOKIES.get('cart', '[]'))
    if cart.count(productId) > 0:
        response = JsonResponse({"code": 1, "message": "Produkt bereits vorhanden", "cart": cart})
        return response
    else:
        cart.append(productId)
        response = JsonResponse({"message": "Produkt hinzugefügt", "cart": cart})
        response.set_cookie("cart", json.dumps(cart), max_age=3600 * 24 * 7)
        return response

@csrf_exempt
def payment_done(request):
    response = render(request, "payment_done.html")
    response.delete_cookie("cart")
    return response

@method_decorator(csrf_exempt, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerGallery'] = HeaderGallery.objects.all()
        return context
    
    def get_queryset(self):
        queryset = Product.objects.filter(ist_verkauft=False)
        sort_field = self.request.GET.get('sort')  

        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(titel__icontains=query) | Q(beschreibung=query)  # Suche in zwei Feldern
            )

        if sort_field:  
            queryset = queryset.order_by(sort_field)
            
    
        return queryset
    
        

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

# Für Paypal
def checkout (request):
    cart = json.loads(request.COOKIES.get("cart", "[]"))
    products =[]
    preisGesamt = 0
    userId = request.user.id
    paypalCustom = {}
    paypalCustom['userId'] = userId
    paypalCustom['cart'] = cart
    versand = VERSAND
    for productId in cart:
        product = Product.objects.get(id=productId)
        products.append(product)
        preisGesamt += product.preis + versand

    paypal_dict = {
        "business": "sb-xjis637545904@business.example.com",
        "amount": str(preisGesamt),
        "item_name": "Testprodukt",
        "invoice": str(uuid.uuid4()),
        "currency_code": "EUR",
        "notify_url": "https://d9b7-145-254-36-25.ngrok-free.app/paypal/ipn/",
        "return_url": request.build_absolute_uri(reverse("payment_done")),
        "cancel_return": request.build_absolute_uri(reverse("product_list")),
        "custom": json.dumps(paypalCustom)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'checkout.html', {'products': products, 'preisGesamt': preisGesamt, 'paypalForm': form, 'user': request.user, 'versandkosten': VERSAND})


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout_session(request):
    userId = request.user.id
    cart = json.loads(request.COOKIES.get("cart", "[]"))
    products =[]
    preisGesamt = 0
    versand = 7
    for productId in cart:
        product = Product.objects.get(id=productId)
        products.append(product)
        preisGesamt += product.preis + versand

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit', 'sofort', 'ideal', 'giropay'],
        metadata={  
            "user_id": request.user.id,  # Nutzer-ID übergeben
            "cart": json.dumps(cart)
        },
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': product.titel,
                    'images': ['https://ec04-145-254-36-25.ngrok-free.app' + product.images.first().image.url]
                },
                'unit_amount': int(product.preis * 100),  # 50€ in Cent
            },
            'quantity': 1,
        }
        for product in products
        ] + [{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Versand',
                },
                'unit_amount': int(VERSAND * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("payment_done")),
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    print(products[0].images.first().image.url)
    return HttpResponseRedirect(session.url)  # Automatische Weiterleitung zur Stripe-Seite


# Stripe Webhook
@csrf_exempt  # Deaktiviert CSRF-Schutz (weil Stripe keine CSRF-Token sendet)
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Webhook-Event überprüfen und entschlüsseln
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # ✅ Erfolgreiches Payment Event verarbeiten
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')
        user = User.objects.get(id = user_id)
        cart= json.loads(session.get('metadata', {}).get('cart'))
        cartItems = [
            Product.objects.get(pk = pid)
            for pid in cart
        ]
        
        # Transaktionsdetails abrufen
        invoice_id = session.get('id')
        email = session.get('customer_email', '')
        amount = session.get('amount_total', 0) / 100  # Cent in Euro umwandeln

        # 💾 In Datenbank speichern
        order = Orders.objects.create(
            invoice=invoice_id,
            user=user,
            betrag=amount,
            status="bezahlt"
        )

        for product in cartItems:
            order.produkt.add(product)
        order.save()

        for id in cart:
            print("produkt")
            # Prüfen, ob das Produkt existiert
            try:
                product = Product.objects.get(pk=id)  # Produkt abrufen
                order.produkt.add(product)
                product.ist_verkauft = True
                product.save()

            except Product.DoesNotExist:
                print(f"Fehler: Produkt mit ID {id} nicht gefunden!")


        print("success")
        return JsonResponse({'status': 'success'})

    print("ignore")
    return JsonResponse({'status': 'ignored'})

def paymentCancel(request):
    return render(request, "payment_cancel.html")

def agb(request):
    file_path = os.path.join(settings.BASE_DIR, "myShop", "static", "agb.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    htmlText = markdown.markdown(text)
    
    return render(request, "agb.html", {'text': htmlText})

def datenschutz(request):
    file_path = os.path.join(settings.BASE_DIR, "myShop", "static", "datenschutz.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    htmlText = markdown.markdown(text)
    
    return render(request, "agb.html", {'text': htmlText})