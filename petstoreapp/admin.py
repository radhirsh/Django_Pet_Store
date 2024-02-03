
from django.contrib import admin
from .models import Product
class ProductAdmin(admin.ModelAdmin):
  list_display=['id','pname','pcost','pdetails','cat','is_active']

admin.site.register(Product)
# Register your models here.
