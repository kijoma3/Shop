from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Orders, Product, UserProfile
from paypal.standard.ipn.signals import valid_ipn_received
import json
from paypal.standard.models import ST_PP_COMPLETED



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == "Completed":
        print("signal")
        invoice_id = ipn.invoice  # Rechnungsnummer
        orderInfo = json.loads(ipn.custom)  # Produkt-ID aus `custom`
        amount = ipn.mc_gross  # Betrag
        payer_email = ipn.payer_email  # Käufer-E-Mail
        user = User.objects.get(id = orderInfo['userId'])
        print('USERID')
        print(User.objects.get(id = orderInfo['userId']))

        print('CART')
        print(orderInfo['cart'])


    # Bestellung in der Datenbank speichern
        order = Orders.objects.create(
                    invoice=invoice_id,
                    betrag=amount,
                    user=user,
                    status="bezahlt"
                )
        order.save()

        for id in orderInfo['cart']:
            print("produkt")
            # Prüfen, ob das Produkt existiert
            try:
                product = Product.objects.get(pk=id)  # Produkt abrufen
                order.produkt.add(product)
                product.ist_verkauft = True
                product.save()

            except Product.DoesNotExist:
                print(f"Fehler: Produkt mit ID {id} nicht gefunden!")
        print(f"Bestellung gespeichert: {order}")