from django.shortcuts import render, redirect

# Create your views here.

from account.models import Customer

from .models import OrderItem, Order

def cart(request):
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    imgs = {}
    for item in items:
        imgs.update({item.id: item.product.images.get(is_main=True).imageURL})
    context = {'order':order, 'imgs': imgs}
    return render(request, 'order/cart.html', context)

def deletefromcart(request, id):
    cartitem = OrderItem.objects.get(id=id)
    cartitem.delete()
    return redirect('cart')