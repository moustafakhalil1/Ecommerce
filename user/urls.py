from django.urls import path,include
from . import views
urlpatterns = [
   path('register/',views.register,name='signup-user'),
   path('logout/',views.logout,name="logout-user"),
   path('cart/',views.cart,name='cart'),
   path('checkout/',views.checkout,name='checkout'),
   path('UpdateItem/',views.updateItem,name='updateItem'),
   path('ProcessOrder/',views.ProcessOrder,name='processOrder'),
  
    
]
