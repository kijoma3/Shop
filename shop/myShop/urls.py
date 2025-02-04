from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('product/', views.addProduct, name='add_product'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)