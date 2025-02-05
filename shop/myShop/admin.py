from django.contrib import admin
from .models import Product, ProductImage, HeaderGallery

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra=1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(HeaderGallery)

