from django.contrib import admin
from .models import Product,ReviewRating,ProductGalery
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGaleryInline(admin.TabularInline):
    model=ProductGalery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','old_price','new_price','stock','modified_date','is_available','slug')
    inlines=[ProductGaleryInline]
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','is_active')
    list_filter=('product')
    list_editable=('is_active',)
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGalery)
