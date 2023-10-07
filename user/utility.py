from products_app.models import *
import json

# process  is 
   #  1- get the custommer by the current user
   #  2-get the order that match that custommer 
   #  3-get all items for that order
   #  4-get total items counts 
   #  5-get total price for all items
   #  6-get shipping status
   # Send  All The  Data To View.py 
def CookieCart(request):
      try:
         cart=json.loads(request.COOKIES['cart'])
      except:
         cart={}  
      items=[]
      ord={'get_Total_items':0,'get_Total_order_price':0,'shipping':False}
      cartitemCoount=0
      total=0
      # get the count of items from cart cookie
      for i in cart:
         try:
               #total items quantity 
               cartitemCoount +=cart[i]['quantity']
               ord['get_Total_items'] += cart[i]['quantity']
            
               #total price for all qauntity
               Product=product.objects.get(id=i)
               total =(Product.ADPric * cart[i]['quantity'])
               ord['get_Total_order_price'] += total

               # get the product details
               item={
                  'product':{
                     'id':Product.id,
                     'PRDName':Product.PRDName,
                     'ADPric':Product.ADPric,
                     'PRDimage':Product.PRDimage,
                  },
                  'quantity':cart[i]['quantity'],
                  'get_totalItem':total,
               }
               
               items.append(item)
               if Product.digital ==False:
                  ord['shipping']=True
         except:
            pass     
      return {'cartitemCoount':cartitemCoount,'ord':ord,'items':items}
def CartData(request):
   if request.user.is_authenticated:
     customer=request.user.custommer
     ord,created=order.objects.get_or_create(customer=customer,complete=False)
     #then  we need to get all the items in that order by 
     items=ord.order_items.all()
     cartitemCoount=ord.get_Total_items
   else:
      CookieData=CookieCart(request)
      cartitemCoount=CookieData['cartitemCoount']
      ord=CookieData['ord']
      items=CookieData['items']
    
   return {'cartitemCoount':cartitemCoount,'ord':ord,'items':items}
def GuestOrder(request ,data):
   
   Name=data['form']['name']
   emaill=data['form']['email']

   print(Name,emaill)

   customer,created=custommer.objects.get_or_create(email=emaill) 
   customer.name=Name
   customer.save()

   cartdata=CookieCart(request)
   print('user didnt log..7')  
   items=cartdata['items']
   print('user didnt log..8')  

   ord=order.objects.create(
      customer=customer,
      complete=False
   )
   print('user didnt log..9')  
   for item in items:
      Product=product.objects.get(id=item['product']['id'])
      orderItem.objects.create(
         product=Product,
         order=ord,
         quantity=item['quantity']
         )
   print('user didnt log..10')  
   return ord,customer