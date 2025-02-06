from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/', views.addProduct, name='add_product'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register', views.register, name='register'),
    path('cart', views.cartView, name='cart'),
    path('addCart/', views.addCartView, name='addCart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)