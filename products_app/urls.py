
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.search,name='search'),
    path('single_product/<slug:slug>',views.single_product,name='single_product'),
   
]
