
import django
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import user
from django.http import JsonResponse
from products_app.models import *
import json
import datetime
# Create your views here.
def register(request):
    if request.method=='POST':
       form=UserCreationForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('user-login')
    else :
        form=UserCreationForm(request.POST)    
    context={
        'form':form,
    }
    return render(request,'user/signup.html',context)



@login_required(login_url='user-login')  
def cart(request):
    
    # if 'product_id' in request.GET and 'quantity' in request.GET and 'product_price' in request.GET :
    #    return redirect('/index/'+ request.GET['product_id'])
    #else:
    #first get the customer and then get or create the order for this custemoer
   if request.user.is_authenticated:
     customer=request.user.custommer
     ord,created=order.objects.get_or_create(customer=customer,complete=False)
     #then  we need to get all the items in that order by 
     items=ord.order_items.all()
     cartitemCoount=ord.get_Total_items
   else:
     items=[]
       
   context={
         'items':items,
         'order':ord,
         'cartitemCoount':cartitemCoount,
     }

   return render(request,'user/cart.html',context)

@login_required(login_url='user-login')     
def updateItem(request):
   data=json.loads(request.body)
   product_id=data['productId']
   action=data['action']
   print('product id : ',product_id)
   print('acion: ',action)
   productn = product.objects.get(id=product_id)

   customer=request.user.custommer
   ord,created=order.objects.get_or_create(customer=customer,complete=False)
   orderItems,created=orderItem.objects.get_or_create(order=ord,product=productn)
   if (action=='add'):
      orderItems.quantity=(orderItems.quantity + 1)
   elif (action=='remove'):
      orderItems.quantity=(orderItems.quantity - 1)
   orderItems.save()    
   if orderItems.quantity <=0:
      orderItems.delete()    
        
   
   return JsonResponse("Item Added succesfully....",safe=False)
   

def checkout(request):
    if request.user.is_authenticated:
       customer=request.user.custommer
       ord,created=order.objects.get_or_create(customer=customer,complete=False)
       items=ord.order_items.all()
       #then  we need to get all the items in that order by 
       cartitemCoount=ord.get_Total_items
      
       total=ord.get_Total_order_price
       shippingg=ord.shipping
    else:
       items=[]
       ordere={'get_Total_items':0,'get_Total_order_price':0,'shipping':False}
       cartitemCoount=ordere['get_Total_items']
       total=ordere['get_Total_order_price']
       shippingg=ordere['shipping']
    context={
       'cartitemCoount':cartitemCoount,
       'items':items,
       'get_Total_order_price':total,
       'shipping':shippingg,
       
    }
    return render(request,'user/checkout.html',context)    


def logout(request):
    return render(request,'user/logout.html')
def ProcessOrder(request):
   transaction_id=datetime.datetime.now().timestamp()
   data=json.loads(request.body)

   if request.user.is_authenticated:
      customer=request.user.custommer
      ord,created=order.objects.get_or_create(customer=customer,complete=False)
      total=float(data['form']['total'])
      ord.transactio_id=transaction_id
      if (total==ord.get_Total_order_price):
         ord.complete=True
   
      ord.save()
      if ord.shipping==True:
         ShppingAdress.objects.create(
            customer=customer,
            order=ord,
            address=data['shipping']['Address'],
            City=data['shipping']['city'],
            State=data['shipping']['state'],
            zibcode=data['shipping']['zibecode'],
         )
      
   else:
      print('user didnt log..')   

   return JsonResponse('Payement Complete....',safe=False)