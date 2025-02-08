from django.contrib import admin
from .models import Product, ProductImage, HeaderGallery, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra=1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False 
    verbose_name_plural = "Zusätzliche Informationen"


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(HeaderGallery)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

