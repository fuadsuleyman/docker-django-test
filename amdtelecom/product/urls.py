from django.urls import path, include
from . import views
from .views import ProductListView
from django.conf.urls.static import static

app_name = 'product'

urlpatterns = [
    # path('', views.home, name='amd-home'),
    path('products/', ProductListView.as_view(), name='products_list'),
    # path('', views.home_page, name='amd-home'),
    # path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),
    # path('products/', views.about, name='amd-about'),
    path('api/v1.0/', include('product.api.urls')),
]