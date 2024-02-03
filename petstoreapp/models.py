from django.db import models

from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
  pname=models.CharField(max_length=50)
  pcost=models.FloatField()
  pdetails=models.CharField(max_length=100)
  cat=models.IntegerField()
  is_active=models.BooleanField(default=True)
  pimage=models.ImageField(upload_to="image" )
  def __str__(self):
    return self.pname

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
