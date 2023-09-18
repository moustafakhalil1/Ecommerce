from django.forms import SlugField
from django.shortcuts import render,redirect
from .models import category, product,product_accessory, productimage
from django.core.paginator import Paginator
from .models import product,cart
from django.contrib.auth.decorators import login_required
from .models import orderItem,order
# Create your views here.

@login_required(login_url='user-login')
def index(request):
    products=product.objects.all()
    Paginatorr=Paginator(products,4) 
    page = request.GET.get("page")
    products=Paginatorr.get_page(page)

    if request.user.is_authenticated:
       customer=request.user.custommer
       ord,created=order.objects.get_or_create(customer=customer,complete=False)
       #then  we need to get all the items in that order by 

       cartitemCoount=ord.get_Total_items
    else:
       ordere={'get_Total_items':0,'get_Total_order_price':0,'shipping':False}
       cartitemCoount=ordere['get_Total_items']

    context={
        'products':products,
        'cat':category.objects.all(),
        'cartitemCoount':cartitemCoount,
        
    }
    return render(request,'products/index.html',context)

@login_required(login_url='user-login')
def single_product(request,slug):
    from .models import cart  
    product_id=product.objects.get(PRDslug=slug)
    accessory=productimage.objects.filter(PRDIproduct=product_id)
   
    if request.method=="POST":
       q=request.POST.get('quantity')
       p=request.POST.get(slug)
       obj=cart(Quantity=q,product=product_id)
       obj.save()
      
    context={
        'singlproduct':product_id,
        'ac':accessory,
    }
    return render(request,'products/single_product.html',context)    

def search(request):
    q=request.GET['query']
    products=product.objects.filter(PRDName__icontains=q)
    context={
        'products':products,     
    }
    return render(request,'products/search.html',context)



