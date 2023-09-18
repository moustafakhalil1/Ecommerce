from email.policy import default
from django.db import models
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class category(models.Model):
    CATName=models.CharField(max_length=100,verbose_name=_('sup category'),null=True,blank=True,) 
    CATParent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,limit_choices_to={'CATParent__isnull':True},blank=True,verbose_name=_('Main category'))    
    CATDescription=models.TextField(max_length=1000)
    CATImg=models.ImageField(upload_to='category_image',null=True,blank=True,)
    def __str__(self) -> str:
        return self.CATName
    class Meta:
        verbose_name=_("category")
        verbose_name_plural=_("categories")     
class product(models.Model):
    PRDName=models.CharField(max_length=100,verbose_name=_('product name'))
    PRDCategory=models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True,verbose_name=_('product category'))
    PRDimage=models.ImageField(upload_to='product_photo',verbose_name='product image',null=True,blank=True)
    PRDBrand=models.ForeignKey('settings.Brand',on_delete=models.CASCADE,null=True,blank=True,verbose_name=_('product brand'))
    PRDDescription=models.TextField(verbose_name=_('product description'))
    PRDPric=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name=_('product pric'))
    ADPric=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name=_('product pric after discount'))
    PRDCost=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name=_('product cost'))
    PRDcreated=models.DateTimeField(verbose_name=_('product date'))
    PRDslug=models.SlugField(null=True,blank=True,)
    PRDnew=models.BooleanField(default=True)
    digital=models.BooleanField(default=True)

    class Meta:
        verbose_name=_("product")
        verbose_name_plural=_("products")  
    
    def save(self,*arg,**kewargs) -> None:
        if not self.PRDslug:
            self.PRDslug=slugify(self.PRDName)

        return super(product,self).save(*arg,**kewargs)
    def __str__(self) -> str:
        return self.PRDName
class productimage(models.Model):
    PRDIproduct=models.ForeignKey(product,on_delete=models.CASCADE,verbose_name=_('product'))
    PRDimage=models.ImageField(upload_to='product_photo',verbose_name='product image')
    def __str__(self) -> str:
        return str(self.PRDIproduct)
  

class product_alternative(models.Model):
    PLANProduct=models.ForeignKey(product,on_delete=models.CASCADE, related_name='main_product',verbose_name=_('product'))
    PLANAlternative=models.ManyToManyField(product, related_name='alternatives',verbose_name=_('product alternatives'))
    class Meta:
        verbose_name=_("product alternatives")
        verbose_name_plural=_("product alternative")   
    def __str__(self) -> str:
        return str(self.PLANProduct)


class product_accessory(models.Model):
    PRDACCProduct=models.ForeignKey(product,on_delete=models.CASCADE, related_name='accessories_product',verbose_name=_('product'))
    PRDACCAlternative=models.ManyToManyField(product, related_name='accessories_alternatives',verbose_name=_('product accessories'))
    PRDACCAlternativeimage=models.ImageField(upload_to='product_photo',verbose_name='product image',null=True,blank=True)
    class Meta:
        verbose_name=_("product accessory")
        verbose_name_plural=_("product accessories")   
    def __str__(self) -> str:
        return str(self.PRDACCProduct)


class cart(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE,verbose_name=_('product name'),null=True,blank=True)
    Quantity=models.IntegerField(null=True,blank=True)
class custommer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name=_('user'))
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return self.name
class order(models.Model):
    customer=models.ForeignKey(custommer,on_delete=models.SET_NULL,null=True,blank=True)
    date_added=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    transactio_id=models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return str(self.id)
    @property
    def shipping(self):
        shipp=False
        orderitems=self.order_items.all()
        for i in orderitems:
            if i.product.digital==False:
                shipp=True
        return shipp        

    @property
    def get_Total_order_price(self):
        orderitem=self.order_items.all()
        total=sum([item.get_totalItem  for item in orderitem ]) 
        return total
    @property
    def get_Total_items(self):
        orderitem=self.order_items.all()
        count=sum([item.quantity for item in orderitem  ]) 
        return count
class orderItem(models.Model):
    product=models.ForeignKey(product,on_delete=models.SET_NULL,null=True,blank=True)
    # i put related name=order_items for get all objects of orderitem from class order
    order=models.ForeignKey(order,on_delete=models.SET_NULL,null=True,blank=True,related_name='order_items')
    date_added=models.DateField(auto_now_add=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self) -> str:
        return str(self.id)   
    @property
    def get_totalItem(self):
        total=(self.product.PRDPric)*self.quantity
        return total  
        


class ShppingAdress(models.Model):
    customer=models.ForeignKey(custommer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(order,on_delete=models.SET_NULL,null=True,blank=True)
    Address=models.CharField(max_length=200,null=False)
    City=models.CharField(max_length=200,null=False)
    State=models.CharField(max_length=200,null=False)
    zip_code=models.CharField(max_length=200,null=False)
    date_added=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.Address

