from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, DetailView

# Create your views here.
from django.http import HttpResponse
from .models import Product, Product_images
from order.models import OrderItem, Order
from account.models import Customer


# products = [
#     {
#         'author': 'Fuad Suleymanov',
#         'title': 'Galaxy S9 Pro',
#         'description': 'So powerfull, so nice',
#         'data_posted': 'October 17, 2020'
#     },
#     {
#         'author': 'Elxan Bayramov',
#         'title': 'Galaxy S10',
#         'description': 'it is so awesome',
#         'data_posted': 'October 16, 2020'
#     },
#     {
#         'author': 'Vaqif Balayev',
#         'title': 'Apple S11',
#         'description': 'just difference',
#         'data_posted': 'October 15, 2020'
#     }

# ]
# Product.objects.all()
# def home(request):
#     context = {
#         'products': Product.objects.all()
#     }
#     return render(request, 'product/home.html', context)

# class ProductListView(ListView):
#     model = Product
#     template_name = 'product/home.html'
#     context_object_name = 'products'
#     ordering = ['-date_posted']

# bu versiya ishleyir
# def home_page(request):
#     products = Product.objects.all()
#     details = Product_details.objects.all()
#     context = {'products':products, 'details': details}
#     return render(request, 'product/home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'product/products.html'
    context_object_name = 'products'
    ordering = ['-created_at']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    photos = Product_images.objects.filter(product=product)
    # details = Product_details.objects.filter(product=product)

    # if request.method == 'POST':
    #     product = Product.objects.get(slug=slug)
    #     device = request.COOKIES['device']
    #     customer, created = Customer.objects.get_or_create(device=device)

    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    #     orderItem.quantity=request.POST['quantity']
    #     orderItem.save()

    #     return redirect('cart')
    context = {'product':product,'photos':photos}

    if request.method == 'POST':
        product = Product.objects.get(slug=slug)
        #Get user account information
        try:
            customer = request.user.customer	
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity=request.POST['quantity']
        orderItem.save()

        return redirect('order:cart')

    return render(request, 'product/product_detail.html', context)



# def about(request):
#     return render(request, 'product/about.html', {'title': 'About'})



