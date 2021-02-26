from django.shortcuts import render
from product.models import Product
# from product.models import Product_details

# Create your views here.


# def home_page(request):
#     products = Product.objects.all()
#     details = Product_details.objects.all()
#     context = {'products':products, 'details': details}
#     return render(request, 'home.html', context)


def index(request):

    # slider_data = SlideInfo.objects.filter(is_full_screen=True)
    # slider_main_data_first = SlideInfo.objects.filter(is_main=True)[:2]
    # slider_main_data_last = SlideInfo.objects.filter(is_main=True)[2:]
    products = Product.objects.all()
    # categories = Category.objects.all()
    # main_cats = Category.objects.filter(is_main=True)
    # second_cats = Category.objects.filter(is_second=True)
    
    # clothing = Category.objects.get(title='Clothing')
    # clothing_childs = Category.objects.filter(parent=clothing).filter(is_third=True)

    # shoes = Category.objects.get(title='Shoes')
    # shoes_childs = Category.objects.filter(parent=shoes).filter(is_third=True)

    # accessories = Category.objects.get(title='Accessories')
    # accessoaries_childs = Category.objects.filter(parent=accessories).filter(is_third=True)

    # asagidaki kodu form tag-e atdim
    # if request.method == 'POST':
    #     form = SubscribeForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         # username = form.cleaned_data.get('username')
    #         messages.success(request, f'Your are subscribed, we will send you emails!')
    #         # return redirect('index_page')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # else:
    #     form = SubscribeForm
    context = {
        # 'slider_data': slider_data,
        # 'slider_main_data_first': slider_main_data_first,
        # 'slider_main_data_last': slider_main_data_last,
        'products': products,
        # 'categories': categories,
        # 'main_categories': main_cats,
        # 'second_categories': second_cats,
        # 'shoes_childs': shoes_childs,
        # 'clothing_childs': clothing_childs,
        # 'accessoaries_childs': accessoaries_childs,
        # 'form': form
    }

    return render(request, 'index/index.html', context)
