from django.urls import path
from . import views
# from .views import ProductListView
from django.conf.urls.static import static

app_name = 'index'

urlpatterns = [
    path('', views.index, name='amd-home'),
]