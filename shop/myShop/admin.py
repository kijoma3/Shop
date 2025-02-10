from django.contrib import admin
from .models import Product, ProductImage, HeaderGallery, UserProfile, Orders
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra=1



class OrdersInline(admin.TabularInline):  # Neues Inline für Orders
    model = Orders
    extra = 0  # Keine leeren zusätzlichen Zeilen
    fields = ['produkt', 'betrag', 'status', 'invoice']
    readonly_fields = ['invoice', 'betrag', 'status', 'produkt'] 


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False 
    verbose_name_plural = "Zusätzliche Informationen"


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline, OrdersInline]


class OrdersAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False  # ✅ Verhindert das Hinzufügen neuer Bestellungen

    def has_change_permission(self, request, obj=None):
        return False  # ✅ Verhindert das Bearbeiten von Bestellungen

    def has_delete_permission(self, request, obj=None):
        return False  # ✅ Verhindert das Löschen von Bestellungen
    
    def produkt(self, obj):
        return ", ".join([product.titel for product in obj.products.all()])
    
    list_display = ("invoice", "user", "produkt", "betrag", "status", "datum")  # Tabellarische Anzeige
    readonly_fields = ("invoice", "user", "produkt", "betrag", "status", "datum")  # Felder nur lesbar


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(HeaderGallery)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

