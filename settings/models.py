
from django.db import models

# Create your models here.
class Brand(models.Model):
    BRDname=models.CharField(max_length=50,verbose_name='brand name')
    BRDdescription=models.TextField(max_length=1000,null=True,blank=True,verbose_name='brand description')
    class Meta:
        verbose_name='brand'
        verbose_name_plural='brands'
    def __str__(self) -> str:
        return str(self.BRDname)


class variant(models.Model):
    VARname=models.CharField(max_length=50,verbose_name='variant name')
    VARdescription=models.TextField(max_length=1000,null=True,blank=True,verbose_name='variant description')
    class Meta:
        verbose_name='variant'
        verbose_name_plural='variants'
    def __str__(self) -> str:
        return str(self.BRDname)