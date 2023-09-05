from django.contrib import admin
from .models import Cart_item,Carts
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','date_added')
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')

admin.site.register(Carts,CartAdmin)
admin.site.register(Cart_item,CartItemAdmin)