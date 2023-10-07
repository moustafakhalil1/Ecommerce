
import django
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import user
from django.http import JsonResponse
from products_app.models import *
import json
import datetime
from .utility import CookieCart ,CartData ,GuestOrder



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

def logout(request):
    return render(request,'user/logout.html')

def cart(request):
   
   CookieData=CartData(request)
   cartitemCoount=CookieData['cartitemCoount']
   ord=CookieData['ord']
   items=CookieData['items']
   context={
         'items':items,
         'order':ord,
         'cartitemCoount':cartitemCoount,
     }

   return render(request,'user/cart.html',context)

   
def updateItem(request):
#process in UpdateItem API 
   # 1-From the Fetch API That is  Sending The Product Id and The action Type
   # when updated-cart class clicked (index.html or checkout.html)
   # 2-get all the data by json.loads(request.body) function
   # 3-get product id  
   # 4-get action
   # 5-get the custommer name by the current user
   # 6-get the order  match the custommer name
   # 7-get the order items by order and the product that is match
   #  if there is no one with that product  order order create new one by------> get_or_create  method
   # 8-if action == add increase the quantity of the item by one
   # if remove decrease it by one 
   # 9-save the process in the database
   # 10-return JsonResponse("Item Added succesfully....",safe=False)
   
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



from django.views.decorators.csrf import csrf_exempt   
@csrf_exempt
def checkout(request):
   CookieData=CartData(request)
   cartitemCoount=CookieData['cartitemCoount']
   ord=CookieData['ord']
   items=CookieData['items']
   context={
       'cartitemCoount':cartitemCoount,
       'items':items,
       'ord':ord,
    }
   return render(request,'user/checkout.html',context)    


# Saving The Shipping Inforamtion (address ,city ,total .....) Into The DataBase 
@csrf_exempt
def ProcessOrder(request):
   transaction_id=datetime.datetime.now().timestamp()
   data=json.loads(request.body)

   if request.user.is_authenticated:
      customer=request.user.custommer
      ord,created=order.objects.get_or_create(customer=customer,complete=False)
   else:
      ord,customer=GuestOrder(request ,data)
      print('user didnt log..11')  

   total=data['form']['total']
   ord.transactio_id=transaction_id
   if (total==ord.get_Total_order_price):
      ord.complete=True
   ord.save()
   if ord.shipping==True:
      ShppingAdress.objects.create(
         customer=customer,
         order=ord,
         Address=data['shipping']['address'],
         City=data['shipping']['city'],
         State=data['shipping']['state'],
         zip_code=data['shipping']['zibcode'],
      )
   return JsonResponse('Payement Complete....',safe=False)