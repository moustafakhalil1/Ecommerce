from django.forms import SlugField
from django.shortcuts import render,redirect
from .models import category, product,product_accessory, productimage
from django.core.paginator import Paginator
from .models import product,cart
from django.contrib.auth.decorators import login_required
from .models import orderItem,order
from user.utility import CookieCart ,CartData
# Create your views here.


def index(request):
    products=product.objects.all()
    Paginatorr=Paginator(products,4) 
    page = request.GET.get("page")
    products=Paginatorr.get_page(page)
    
    CookieData=CartData(request)
    cartitemCoount=CookieData['cartitemCoount']

    context={
        'products':products,
        'cat':category.objects.all(),
        'cartitemCoount':cartitemCoount,
        
    }
    return render(request,'products/index.html',context)


def single_product(request,slug):
    from .models import cart  
    product_id=product.objects.get(PRDslug=slug)
    accessory=productimage.objects.filter(PRDIproduct=product_id)

    CookieData=CartData(request)
    cartitemCoount=CookieData['cartitemCoount']
    ord=CookieData['ord']
    items=CookieData['items']
  
    context={
        'items':items,
        'order':ord,
        'cartitemCoount':cartitemCoount,
        'singlproduct':product_id,
        'ac':accessory,
    }
    return render(request,'products/single_product.html',context)    





